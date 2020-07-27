# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Box
from gent import GameObject
from gent import TextLine
from gent import TextBox

class Controls(GameObject):
    '''
    Display a single card
    '''

    def __init__(self):
        GameObject.__init__(self, Box(0, 14, 54, 5))

        self.hint: TextBox = TextBox(Box(0, 0, self.w, 2), "Try to get closer to 21 than the\ndealer without going over!", (255, 255, 255), (60, 15, 90), justify="C")

        self.controlHint: TextLine = TextLine(Box(0, 3, self.w, 1), "Press (RETURN) to hit and (SPACE) to stay.", (255, 255, 255), (60, 15, 90), justify="C")
        self.navHint: TextLine = TextLine(Box(0, 4, self.w, 1), "Press (TAB) to return to main menu.", (255, 255, 255), (60, 15, 90), justify="C")
    
    def render(self):
        self.bufferCanvas.backgroundColors[:,:] = (60, 15, 90)

        self.hint.drawOn(self)

        self.controlHint.drawOn(self)
        self.navHint.drawOn(self)
