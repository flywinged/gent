from ..internal import Event, timeFunction, Box, EVENT_HANDLER

from ..utilities import recursiveSplit

from .textBox import TextBox

from typing import Tuple

import numpy

class InputBox(TextBox):
    '''

    '''
    def __init__(self, box: Box, textColor: tuple, backgroundColor: tuple, cursorTextColor: tuple, cursorBackgroundColor: tuple, cursorBlinkSpeed: float = 1.0, justify: str = "L", **kwargs):
        TextBox.__init__(self, box, "", textColor, backgroundColor, justify = justify, **kwargs)

        # Copy initialization parameters
        self.cursorTextColor: tuple = cursorTextColor
        self.cursorBackgroundColor: tuple = cursorBackgroundColor
        self.cursorBlinkSpeed: float = cursorBlinkSpeed

        # Determine the maximum number of characters the text box can hold
        self.maximumCharacters: int = self.w * self.h

        # Where the current input position is
        self.cursor: int = 0
        self.cursorPosition: Tuple[int, int] = (0, 0)
        self.realCursorPosition: Tuple[int, int] = (0, 0)

        # Timing mechanism
        self.t: float = timeFunction()

        # Initialize the textLine objects
        self.updateCursorIndex(0)

        # Whether or not the input box needs to update where the cursor currently is
        self.updateCursor: bool = True
    
    def _handleEvent(self, event: Event):
        '''

        '''
            
        # Move the cursor
        if event.keyName in {"UP", "DOWN", "LEFT", "RIGHT", "HOME", "END"}:
            self.moveCursor(event.keyName)

        # If the character is backspace, then the replacement is an empty space and the previous location needs to be removed
        elif event.keyName == "BACKSPACE" or event.keyName == "DELETE":
            
            if event.keyName == "DELETE":
                if self.cursor == len(self.text):
                    return EVENT_HANDLER.HANDLED
                
                self.updateCursorIndex(1)

            # Replace the appropriate part of the string
            if self.cursor != 0:
                self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
            else:
                self.text = ""
            
            self.updateCursorIndex(-1)
            return EVENT_HANDLER.HANDLED
        
        else:

            # Determine what the character to add is.
            characterReplacement = event.char
            
            # Only add characters if the are of length one (example, don't write "CapsLock").
            # Also don't add any characters if the cursor is at the end of the text
            if characterReplacement and len(characterReplacement) == 1 and ord(characterReplacement) < 256 and event.keyName != "RETURN" and event.keyName != "ESCAPE" and event.keyName != "TAB":

                text = self.text[:self.cursor] + characterReplacement + self.text[self.cursor:]

                # Determine if we can add the letter or not
                lines = recursiveSplit(text, self.w)
                canAdd = True
                if len(lines) > self.h:
                    canAdd = False
                for line in lines:
                    if len(line) > self.w and (len(line) > 0 and line[-1] not in {" ", "\n"}):
                        canAdd = False
                    if len(line) > self.w + 1:
                        canAdd = False

                # Only add the text if the string stays within the bounds of the text box.
                if canAdd:
                    self.text = text
                    self.updateCursorIndex(1)
                    return EVENT_HANDLER.HANDLED

    def moveCursor(self, direction: str):
        '''
        Move the cursor up down left or right. (Also has the functionality built in for Home and End)
        '''

        def searchForPosition(target: Tuple[int]):
            '''
            Search for a specific cursor position
            '''

            # Loop through each of the available positions the cursor could be in
            for i in range(len(self.text)):
                xIndex, yIndex = self.getCursorPosition(index = i)

                # Select the one which allows the target value to be matched
                if (xIndex, yIndex) == target:
                    self.cursor = i
                    self.updateCursorIndex(0)
                    return True
            
            # If nothing was found, return false
            return False

        # Move the cursor one to the right
        if direction == "RIGHT":
            self.updateCursorIndex(1)

        # Move the cursor one to the left
        elif direction == "LEFT":
            self.updateCursorIndex(-1)
        
        # Move the cursor up in the text box
        elif direction == "UP":
            if searchForPosition((self.cursorPosition[0], self.cursorPosition[1] - 1)) == False:
                self.cursor = 0
                self.updateCursorIndex(0)
        
        # Move the cursor down in the text box
        elif direction == "DOWN":
            if searchForPosition((self.cursorPosition[0], self.cursorPosition[1] + 1)) == False:
                self.cursor = len(self.text)
                self.updateCursorIndex(0)

        # Send the cursor to the begining of the box
        elif direction == "HOME":
            self.updateCursorIndex(-self.cursor)
        
        # Send the cursor to the end of the box
        elif direction == "END":
            self.updateCursorIndex(len(self.text) - self.cursor)
    
    def getCursorPosition(self, index = None):
        '''
        Determine the x, y position of the cursor in the gameObject.
        '''
        
        # Defaults to getting the current cursor position, but can request the value of any index
        if index == None:
            index = self.cursor

        # Wrapper function to make use of return sequence as well as make logic easier to read
        def getPosition():
            '''
            Get the xIndex and yIndex for the current cursor position
            '''

            # x, y position in the gameObject
            xIndex, yIndex = 0, -1

            # How many characters have currently been searched through. Stop the algorithm when characterCount = index
            characterCount = 0

            # Loop through each textLine
            for i in range(len(self.textLineDataList)):
                text = self.textLineDataList[i].textLine.text
                
                # Don't count any of the lines which don't contain text
                if len(text) == 0:
                    continue

                # When moving to a new textLine, the yIndex increases and the xIndex is reset
                yIndex += 1
                xIndex = 0
                
                # Loop through each of the characters in the textLine.
                for _ in range(len(text)):

                    # Each new character moves along one position in the xDirection
                    xIndex += 1    
                    characterCount += 1

                    # Stop searching as soon as character count
                    if characterCount == index:
                        if xIndex >= self.w:
                            xIndex = 0
                            yIndex += 1

                        return xIndex, yIndex
            
            return xIndex, yIndex

        xIndex, yIndex = getPosition()

        # Adjust given the justification
        if yIndex < self.h:
            xIndex += self.textLineDataList[yIndex].textLine.lineStart

        if xIndex >= self.w:
            xIndex = self.w - 1
        if yIndex >= self.h:
            yIndex = self.h - 1

        if index == 0:
            
            if self.justify == "L":
                xIndex, yIndex = 0, 0
        
        return xIndex, yIndex

    def updateCursorIndex(self, increment: int):
        '''

        '''

        # First, move the cursor
        self.cursor += increment
        if self.cursor < 0:
            self.cursor = 0
        if self.cursor > len(self.text):
            self.cursor = len(self.text)

        self.updateCursor = True

    def updatecursorPosition(self):
        '''
        Updates the x, y position of the cursor within the textbox
        '''

        self.cursorPosition = self.getCursorPosition()
        self.realCursorPosition = self.cursorPosition[0] + self.xOffset, self.cursorPosition[1] + self.yOffset
        
    def _setValues(self):
        TextBox._setValues(self)

        # If the cursor position needs to be updated (such as when text is added)
        if self.updateCursor:
            self.updateCursor = False
            self.updatecursorPosition()

        # Draw the blinking cursor
        if self.selectionStatus == self.SELECTED and ((timeFunction() - self.t) // (self.cursorBlinkSpeed / 2)) % 2 == 0:
            self.bufferCanvas.backgroundColors[self.realCursorPosition] = numpy.array(self.cursorBackgroundColor)
            self.bufferCanvas.textColors[self.realCursorPosition] = numpy.array(self.cursorTextColor)
        else:
            self.bufferCanvas.backgroundColors[self.realCursorPosition] = numpy.array(self.backgroundColor)
            self.bufferCanvas.textColors[self.realCursorPosition] = numpy.array(self.textColor)
        