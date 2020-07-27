# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Box
from gent import GameObject
from gent import Game
from gent import Event

from .hand import Hand
from .controls import Controls

from ...state import STATE

class GameScreen(GameObject):
    '''
    The start screen contains the blackjack background image and user options.
    '''

    def __init__(self, game: Game):
        GameObject.__init__(self, Box(0, 0, 54, 19), game = game)
        # self.addObjectHandler()

        playerBox = Box(0, 0, 26, 12)
        self.playerHand: Hand = Hand(playerBox, STATE.playerCards, "Player")

        dealerBox = Box(28, 0, 26, 12)
        self.dealerHand: Hand = Hand(dealerBox, STATE.dealerCards, "Dealer")

        self.controls: Controls = Controls()
    
    def onExit(self):
        self.game.goToScreen("Start")
    
    def handleEvent(self, event: Event):

        if event.keyName == "RIGHT":
            STATE.hit("player")
        
        if event.keyName == "TAB":
            self.game.goToScreen("Start")
    
    def render(self):

        self.bufferCanvas.backgroundColors[:,:] = (60, 15, 90)
        self.bufferCanvas.backgroundColors[26:28, :] = (80, 20, 110)
        self.bufferCanvas.backgroundColors[:,13] = (80, 20, 110)
        
        self.playerHand.drawOn(self)
        self.dealerHand.drawOn(self)

        self.controls.drawOn(self)
