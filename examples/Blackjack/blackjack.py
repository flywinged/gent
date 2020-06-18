# Copyright Clayton Brown 2019. See LICENSE file.

from gent import GameState

# Typings
from typing import List

from dataclasses import dataclass
import random

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
        for suit in ["Clubs", "Spades", "DIamonds", "Hearts"]:
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

class BlackJackState(GameState):
    '''
    Contains deck info for playing blackjack
    '''

    def __init__(self):
        GameState.__init__(self)

        self.deck: List[CardData] = []

        self.dealerCards: List[CardData] = []
        self.playerCards: List[CardData] = []
    
    def deal(self):

        # Create/Shuffle deck
        self.deck = createDeck()

        # Deal the player and the dealer two cards.
        self.playerCards.append(self.deck.pop(0))
        self.dealerCards.append(self.deck.pop(0))
        self.playerCards.append(self.deck.pop(0))
        self.dealerCards.append(self.deck.pop(0))



from gent import GameObject
from gent import Box

from typing import Tuple

class Card(GameObject):
    '''

    '''

    def __init__(self, position: Tuple[int], cardData: CardData):
        GameObject.__init__(self, Box(position[0], position[1], 20, 15))

        self.data: CardData = cardData
    
    def _setValues(self):
        '''

        '''

        self.bufferCanvas.backgroundColors.fill(50)


from gent import Game
def run():

    gs = BlackJackState()
    gs.deal()
    g = Game(gs, (120, 40))

    c = Card((0, 0), CardData(5, "Five", "Clubs"))
    g.addGameObject(c)

    g.gameLoop()