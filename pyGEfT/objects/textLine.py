from ..internal import GameObject, Box

import numpy

class TextLine(GameObject):
    '''

    '''

    def __init__(self, box: Box, text: str, textColor: tuple, backgroundColor: tuple, justify = "L", **kwargs):
        
        # TextLine object are only able to have a height of one
        box.h = 1
        GameObject.__init__(self, box, **kwargs)

        # Assign default parameters
        self.text: str = text
        self.textColor: tuple = textColor
        self.backgroundColor: tuple = backgroundColor
        self.justify: str = justify

        # Keep track of where the start and end of this textLine are
        self.lineStart: int = 0
        self.lineEnd: int = 0

    def _setValues(self):

        self.bufferCanvas.clearCanvas()

        # Create adjusted text to ignore the trailing space
        adjustedText = self.text
        if len(adjustedText) > 0 and (adjustedText[-1] == " " or adjustedText[-1] == "\n"):
            adjustedText = adjustedText[:-1]

        # Determine where the text needs to start to handle the justification
        startIndex = 0
        if self.justify == "R":
            startIndex = self.w - len(adjustedText)
        elif self.justify == "C":
            startIndex = (self.w - len(adjustedText)) // 2
        
        # Loop through all the text values and assign the correct characters
        for i in range(min(len(adjustedText), self.w)):
            self.bufferCanvas.characters[startIndex + i, 0] = ord(adjustedText[i])
        
        # Update the start and end values for the textLine
        self.lineStart = startIndex
        self.lineEnd = startIndex + len(self.text)

        # Set the text color and background
        self.bufferCanvas.textColors[:,:] = numpy.array(self.textColor)
        self.bufferCanvas.backgroundColors[:,:] = numpy.array(self.backgroundColor)