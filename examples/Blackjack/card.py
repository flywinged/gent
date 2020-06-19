# Copyright Clayton Brown 2019. See LICENSE file.

from dataclasses import dataclass
import random

from typing import List, Tuple

from gent import GameObject, Box, TextLine

@dataclass
class CardData:

    value: int
    name:  str
    suit:  str

def createDeck() -> List[CardData]:
    '''
    Create a new shuffled deck
    '''

    deck = []

    for value in range(1, 14):
        for suit in ["Clubs", "Spades", "Diamonds", "Hearts"]:
            cardName = {
                1: "Ace",
                2: "Two",
                3: "Three",
                4: "Four",
                5: "Five",
                6: "Six",
                7: "Seven",
                8: "Eight",
                9: "Nine",
                10:"Ten",
                11:"Jack",
                12:"Queen",
                13:"King"
            }[value]

            deck.append(CardData(
                value,
                cardName,
                suit
            ))
    
    random.shuffle(deck)

    return deck

class Card(GameObject):
    '''

    '''

    def __init__(self, position: Tuple[int], cardData: CardData):
        GameObject.__init__(self, Box(position[0], position[1], 20, 15))

        self.data: CardData = cardData

        self.cardName: TextLine = TextLine(
            Box(0, 0, 20, 1),
            self.data.name + " Of " + self.data.suit,
            (180, 180, 180),
            (40, 40, 40),
            justify="C"
        )
    
    def _setValues(self):
        '''

        '''

        self.bufferCanvas.backgroundColors.fill(15)

        self.cardName.drawOn(self)