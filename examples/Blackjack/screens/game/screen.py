# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Box
from gent import GameObject
from gent import Game

from .hand import Hand

from ...state import STATE

class GameScreen(GameObject):
    '''
    The start screen contains the blackjack background image and user options.
    '''

    def __init__(self, game: Game):
        GameObject.__init__(self, Box(0, 0, 80, 32), game = game)
        self.addObjectHandler()

        playerBox = Box(0, 0, 24, 12)
        self.playerHand: Hand = Hand(playerBox, STATE.playerCards)

        dealerBox = Box(56, 0, 24, 12)
        self.dealerHand: Hand = Hand(dealerBox, STATE.dealerCards)
    
    def onExit(self):
        self.game.goToScreen("Start")
    
    def setValues(self):
        
        self.playerHand.drawOn(self)
        self.dealerHand.drawOn(self)
