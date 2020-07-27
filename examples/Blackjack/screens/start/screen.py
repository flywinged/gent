# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Box
from gent import GameObject
from gent import loadPNG

START_IMAGE = loadPNG("examples/Blackjack/resources/homeScreen.png", (54, 19))

class StartScreen(GameObject):
    '''
    The start screen contains the blackjack background image and user options.
    '''

    def __init__(self):
        GameObject.__init__(self, Box(0, 0, 54, 19))
        self.addObjectHandler()
        self.exitable = False
    
    def render(self):

        self.bufferCanvas.drawImage(START_IMAGE)