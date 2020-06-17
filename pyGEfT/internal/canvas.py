from typing import List

import numpy

import platform

from sty import fg, bg

class Canvas:
    '''
    The Canvas class holds all the screen information necessary to draw in the terminal.

    Parameters
    ----------
    width, height: The width and the height of the canvas in characters.
    '''       

    def __init__(self, width: int, height: int):
        
        # Hold the width and height variables for use elsewhere
        self.width: int = width
        self.height: int = height

        # Create the character and format arrays
        self.characters: numpy.ndarray = numpy.zeros((self.width, self.height), dtype = numpy.uint16)
        self.textColors: numpy.ndarray = numpy.zeros((self.width, self.height, 3), dtype = numpy.uint8)
        self.backgroundColors: numpy.ndarray = numpy.zeros((self.width, self.height, 3), dtype = numpy.uint8)

        # Populate the character and format arrays with default values
        self.clearCanvas(" ", 0)
    
    def clearCanvas(self, clearCharacter: str = " ", textColor: tuple = (255, 255, 255), backgroundColor: tuple = (0, 0, 0)):
        '''
        Assign format and character values to the entire canvas at once
        '''

        # Replace the canvas characters and formats at each "pixel" location
        self.characters.fill(ord(clearCharacter))
        self.textColors[:,:] = numpy.array(textColor)
        self.backgroundColors[:,:] = numpy.array(backgroundColor)

    def getCanvasText(self):
        '''
        Return a string representation of the canvas. This string is what will be printed for visuals.
        '''

        # Allocated all the memory for the string right at the start
        resultingString: List[str] = [""] * (self.width * self.height + 2)

        # Loop through all the characters of both the string and the formatString, and create the resulting string list
        previousTextColor = None
        previousBackgroundColor = None
        for j in range(self.height):
            for i in range(self.width):
            
                character = chr(self.characters[i, j])

                textColor = tuple(self.textColors[i, j])
                backgroundColor = tuple(self.backgroundColors[i, j])

                if not previousTextColor or textColor != previousTextColor:
                    character = fg(*textColor) + character
                    previousTextColor = textColor

                if not previousBackgroundColor or backgroundColor != previousBackgroundColor:
                    character = bg(*backgroundColor) + character
                    previousBackgroundColor = backgroundColor

                # If at the beginning of the line, need to include a new line \n to the character
                if i == 0:

                    if "win" in platform.system().lower():
                        character = "\n" + character
                    else:
                        character = character

                resultingString[j * self.width + i] = character

        # Clear the terminal format after each draw
        resultingString[-2] = bg.rs
        resultingString[-1] = fg.rs

        # Add the last
        return "".join(resultingString)

