import numpy

from types import FunctionType
from csaps import UnivariateCubicSmoothingSpline

class ProbabilityDistribution:
    '''
    Function to handle probability distributions.

    Parameters
    ----------

    distributionFunction:
        FunctionType which takes in a single float value and returns a second float value.
        Describes a distribution function on the interval (0-1).
        Function is not required to have an area of 1 in the interval (0-1), that interval is autmatically generated for you.
        Function must not be negative in the range (0-1). (Negative probability doesn't make much sense anyway)
    '''

    def __init__(self, distributionFunction: FunctionType):

        # Object Variables #
        # Function describing how the distribution should look.
        self.distributionFunction: FunctionType = None

        # The total area of the distribution function between 0 and 1
        self.areaModulation: float = None

        # The approximated integral for the distribution function between 0 and 1
        # This spline is also inverted. This means self.integralSpline(p), where p is between 0 and 1,
        #   returns the x value where p percent of the area under the curve of self.distributionFunction in the range (0-1) is to the left.
        self.integralSpline: UnivariateCubicSmoothingSpline = None

        # Set the apropriate distribution function
        self.setDistributionFunction(distributionFunction)

    def setDistributionFunction(self, distributionFunction: FunctionType, N: int = int(1e5)):
        '''
        Assigns the appropriate distribution function and calculates the integralSpline necessary to match that distribution function.

        Parameters
        ----------
        distributionFunction:
            Districution function to create integral spline for.

        N:
            Number of points to use to create the spline approximation.
            Larger N (N > 1e5) will slow down initial generation, but be more accurate.
            Smaller N (N < 1e3) will speed up geenration significantly, but for complex functions will los accuracy.
        '''

        self.distributionFunction = distributionFunction

        # Create the xData. This is just a linspace between 0 and 1.
        # xData2 is a version of this which is offset by one index to allow for the builtin map function to work for area generation
        xData1 = numpy.linspace(0.0, 1.0, num = N + 1)
        xData2 = numpy.roll(xData1, -1)

        # Create the yData. This maps the xData values at each point to self.distributionFunction(x).
        # Also create the yData2 variable which is equivalent to the xData2, but for yValues
        yData1 = numpy.array(list(map(self.distributionFunction, xData1)))
        yData2 = numpy.roll(yData1, -1)

        # Simple area function to use with map. Use midpoint approach.
        def areaFunction(x1, x2, y1, y2):
            return (x2 - x1) * (y1 + y2) / 2

        # Get a numpy array of the areas of each trapezoid
        areas = numpy.array(list(map(areaFunction, xData1[:-1], xData2[:-1], yData1[:-1], yData2[:-1])))

        # areaModulation describes the total area underneath the probability distribution in the range (0-1)
        self.areaModulation = numpy.sum(areas)

        # Calculate the total area (the integral) at each xValue
        totalAreas = numpy.zeros((N + 1,))
        for i in range(totalAreas.shape[0] - 1):
            totalAreas[i + 1] = totalAreas[i] + areas[i]

        # Use those areas to create the integral spline
        self.integralSpline = UnivariateCubicSmoothingSpline(totalAreas, xData1)
    
    def __call__(self, n: int = 1):
        '''
        Generate random numbers according to the loaded distribution.

        Parameters
        ----------

        n: the number of random numbers to generate. If n == 1: will return a float instead of a numpy array
        '''

        # Create the random numbers accoring the integral spline.
        randomNumbers = self.integralSpline(numpy.random.random((n,)) * self.areaModulation)

        # Return type float if n is set to 1
        if n == 1:
            return randomNumbers[0]
        
        # Otherwise just return a numpy array of random values according to the desired probability distribution.
        return randomNumbers


# Testing call
if __name__ == "__main__":

    from matplotlib import pyplot as plt

    def lightnesDistribution(x): return (.5 - abs(x - .5))**2
    def chromaDistribution(x): return x

    D = ProbabilityDistribution(chromaDistribution)

    plt.hist(D(10000000), 250)
    plt.show()
