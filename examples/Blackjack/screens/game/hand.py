# Copyright Clayton Brown 2019. See LICENSE file.

from ...state import CardData

from typing import List, Tuple

from gent import Box
from gent import GameObject
from gent import TextLine

from ...state import STATE

class CardDisplay(GameObject):
    '''
    Display a single card
    '''

    def __init__(self, box: Box):
        GameObject.__init__(self, box)
    
        self.name: TextLine = TextLine(Box(2, 0, box.w - 2, 1), "", (255, 255, 255), (60, 15, 90), justify="C")

        self.suitColor: Tuple[int] = (0, 0, 0)

    def setCard(self, cardData: CardData, hide: bool = False):
        '''
        Reset all the text values for the text box and the suit indicator
        '''
        
        self.suitColor = (255, 0, 0)
        if cardData.suit == "Spades": self.suitColor = (0, 0, 0)
        if cardData.suit == "Diamonds": self.suitColor = (30, 30, 210)
        if cardData.suit == "Clubs": self.suitColor = (30, 210, 30)
        
        if hide:
            self.suitColor = (60, 15, 90)
            self.name.text = "Hidden"

        else:
            self.name.text = " " + cardData.name + " of " + cardData.suit
            
        self.name.rerender()

    def render(self):
        
        self.name.drawOn(self)
        self.bufferCanvas.backgroundColors[:2, :] = self.suitColor

class Hand(GameObject):
    '''
    The start screen contains the blackjack background image and user options.
    '''

    def __init__(self, box: Box, cardList: List[CardData], player: str):
        GameObject.__init__(self, box)

        self.cardList: List[CardData] = cardList
        self.player: TextLine = TextLine(Box(0, 0, self.w, 1), player, (255, 255, 255), (60, 15, 90), justify="C")
        self.cardTotal: TextLine = TextLine(Box(0, 1, self.w, 1), "", (255, 255, 255), (60, 15, 90), justify="C")

        self.cardObjects: List[CardDisplay] = []
        for y in range(3, self.h):
            textBox = Box(2, y, self.w - 2, 1)
            self.cardObjects.append(CardDisplay(textBox))
    
    def render(self):

        self.bufferCanvas.backgroundColors[:,:] = (60, 15, 90)

        self.player.drawOn(self)

        if self.player.text == "Player":
            self.cardTotal.text = "Total: " + str(STATE.playerCardTotal)
        else:
            self.cardTotal.text = "Total: " + str(STATE.dealerCardTotal)
        self.cardTotal.rerender()
        self.cardTotal.drawOn(self)

        for y in range(len(self.cardList)):

            hide = False
            if y == 0 and self.player.text == "Dealer" and STATE.turn == "player":
                hide = True

            data = self.cardList[y]
            self.cardObjects[y].setCard(data, hide=hide)
            self.cardObjects[y].rerender()
            self.cardObjects[y].drawOn(self)