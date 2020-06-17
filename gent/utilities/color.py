class Color:
    '''
    Class for handling colors. Create and transition between them very easily.
    '''

    def __init__(self):

        self.r: float = 0
        self.g: float = 0
        self.b: float = 0

    def getRGB(self):
        return (round(self.r * 255), round(self.g * 255), round(self.b * 255))

    def getHSL(self):
        pass

    def getHCL(self):
        pass

    def __repr__(self):

        return "Color: (%i,%i,%i)" % (self.getRGB())
    
def mixColors(c1: Color, c2: Color, mixParameter: float):
    '''
    Mix two different colors together

    Parameters
    ----------
    c1/2: The first and second color to mix together

    mixParameters: At 0, the resulting color is c1. At 1, the resulting color is c2
    '''

    color = Color()

    # Mixing is just averaging the color values together
    color.r = c1.r * (1.0 - mixParameter) + c2.r * mixParameter
    color.g = c1.g * (1.0 - mixParameter) + c2.g * mixParameter
    color.b = c1.b * (1.0 - mixParameter) + c2.b * mixParameter

    return color

def createRGB(r: float, g: float, b:float):
    '''
    create an RGB color
    '''

    color = Color()

    color.r = r
    color.g = g
    color.b = b

    return color

def createFromHue(h:float):
    '''
    Create a color based only off hue
    '''

    color = Color()
    
    # There are six different ways for hues to be combined
    sixth = 1/6

    # Transitioning from red to yellow
    if h < sixth:
        color.r = 1.0
        color.g = h / sixth
    
    # Transitioning from yellow to green
    elif h < 2 * sixth:
        color.r = 1.0 - (h - sixth) / sixth
        color.g = 1.0

    # Transitioning from green to cyan
    elif h < 3 * sixth:
        color.g = 1.0
        color.b = (h - 2 * sixth) / sixth
    
    # Transitioning from cyan to blue
    elif h < 4 * sixth:
        color.g = 1.0 - (h - 3 * sixth) / sixth
        color.b = 1.0
    
    # Transitioning from blue to magenta
    elif h < 5 * sixth:
        color.r = (h - 4 * sixth) / sixth
        color.b = 1.0
    
    # Transitioning from magenta to red
    elif h < 6 * sixth:
        color.r = 1.0
        color.b = 1.0 - (h - 5 * sixth) / sixth

    return color

def createHSL(h: float, s: float, l: float):
    '''
    Hue saturation lightness
    '''

    # Start with the base hue
    H = createFromHue(h)

    # Now include lightness
    mixColor = Color()
    if l > .5:
        mixColor = createRGB(1.0, 1.0, 1.0)
    mixAmount = abs(l - .5) / .5
    HL = mixColors(H, mixColor, mixAmount)

    # Then consider saturation
    saturationColor = createRGB(l, l, l)
    HSL = mixColors(HL, saturationColor, 1.0 - s)

    return HSL

def createHCL(h: float, c: float, l: float):
    '''
    Hue, Chroma, Lightness
    '''

    # Start with the base hue
    H = createFromHue(h)

    # Now include lightness
    mixColor = Color()
    if l > .5:
        mixColor = createRGB(1.0, 1.0, 1.0)
    mixAmount = abs(l - .5) / .5
    HL = mixColors(H, mixColor, mixAmount)

    # Determine the current range of color values
    maxValue = max([HL.r, HL.g, HL.b])
    minValue = min([HL.r, HL.g, HL.b])
    colorRange = maxValue - minValue

    # If the desired chroma component is too high, just return the current color
    if colorRange < c: return HL

    # Mix the appropriate amount of chroma in 
    chromaColor = createRGB(l, l, l)
    mixRatio = 1.0 - c / colorRange
    HCL = mixColors(HL, chromaColor, mixRatio)
    
    return HCL
