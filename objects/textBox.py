from ..internal import GameObject, Box
from ..utilities import recursiveSplit

from .textLine import TextLine

from typing import List

from dataclasses import dataclass

@dataclass
class TextLineData:
    '''
    Handles the meta information necessary for the text line data
    '''

    # TextLine object
    textLine: TextLine = None
    
    # Which position in the original textBox text this textLineData starts at
    textIndex: int = 0


class TextBox(GameObject):
    '''
    TextBoxes are a gameobject which display text at a certain position on a canvas.

    Parameters
    ----------
    x, y: Position of the text box on the screen

    text: The text the TextBox is displaying on the screen

    characterStyle: Character style object used to get the style. The character is ignored

    justify: "L", "R", or "C". (Left, Right, or Center). Justifies the text display in the texBox. If a value is ommitted or incorrectly given, will left justify
    '''

    def __init__(self, box: Box, text: str, textColor: tuple, backgroundColor: tuple, justify: str = "L", **kwargs):
        GameObject.__init__(self, box, **kwargs)

        # Set the initialization paramters
        self.text: str = text
        self.textColor: tuple = textColor
        self.backgroundColor: tuple = backgroundColor
        self.justify: str = justify

        # A List of text lines for each line in the textBox
        self.textLineDataList: List[TextLineData] = []
        for i in range(self.h):
            textLineBox = Box(0, i, self.w, 1)
            textLine = TextLine(textLineBox, "", self.textColor, self.backgroundColor, justify = self.justify)
            self.textLineDataList.append(TextLineData(textLine, 0))
        
        self.clearText()

    def clearText(self):

        for textLineData in self.textLineDataList:
            textLineData.textLine.text = ""
            textLineData.textLine.setValues()
            textLineData.textIndex = 0

    def _setValues(self): #pylint: disable=arguments-differ
        '''
        **kwargs
            lines: Presplit text data
        '''

        # Get all the text to split
        lines = recursiveSplit(self.text, self.w)

        # Keep track of the start index for each line
        lineStart = 0
        for i in range(len(self.textLineDataList)):
            textLineData = self.textLineDataList[i]

            if i < len(lines):
                textLineData.textIndex = lineStart
                textLineData.textLine.text = lines[i]

                lineStart += len(lines[i])
            
            else:
                textLineData.textLine.text = ""
                textLineData.textIndex = (i - len(lines)) * self.w + lineStart
            
            textLineData.textLine.setValues()
            textLineData.textLine.draw(self.bufferCanvas, (self.xOffset, self.yOffset))
        