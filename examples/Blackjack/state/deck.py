# Copyright Clayton Brown 2019. See LICENSE file.

from dataclasses import dataclass
import random

from typing import List

@dataclass
class CardData:

    value: int
    name:  str
    suit:  str

class Deck:
    '''
    Object which contains all the card in a deck (Can have any number of cards in it)
    '''

    def __init__(self):

        self.cards: List[CardData] = []
        self.reset()
    
    def reset(self):
        '''
        Repopulate self.cards with an ordered deck
        '''

        self.cards = []

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

                self.cards.append(CardData(
                    value,
                    cardName,
                    suit
                ))
    
    def shuffle(self):
        random.shuffle(self.cards)