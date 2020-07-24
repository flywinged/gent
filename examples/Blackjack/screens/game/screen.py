# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Box
from gent import GameObject
from gent import loadPNG
from gent import Game

class GameScreen(GameObject):
    '''
    The start screen contains the blackjack background image and user options.
    '''

    def __init__(self, game: Game):
        GameObject.__init__(self, Box(0, 0, 80, 32))
        self.addObjectHandler()
    
    def onExit(self):
        self.game.goToScreen("Start")