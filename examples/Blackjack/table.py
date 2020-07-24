# Copyright Clayton Brown 2019. See LICENSE file.

from .card import Card

from .gameState import STATE

from typing import List

from gent import GameObject, Box

class Table(GameObject):
    '''

    '''

    def __init__(self):
        '''

        '''

        GameObject.__init__(self, Box(0, 0, 180, 40))

        # Create 4 cards

        self.playerCards: List[Card] = []
        self.dealerCards: List[Card] = []

        self.setCards()

    def setCards(self):

        for i in range(len(STATE.playerCards)):
            self.playerCards.append(Card(
                (i * 24 + 2, 23),
                STATE.playerCards[i]
            ))
        
        for i in range(len(STATE.dealerCards)):
            self.dealerCards.append(Card(
                (i * 24 + 2, 1),
                STATE.dealerCards[i]
            ))

    def setValues(self):
        '''

        '''

        self.bufferCanvas.backgroundColors.fill(0)

        card: Card
        for card in self.playerCards:
            card.drawOn(self)
        
        for i, card in enumerate(self.dealerCards):
            if i == 0:
                card.state = "hidden"
            card.drawOn(self)