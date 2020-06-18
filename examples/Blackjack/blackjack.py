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

    def hit(self, player: str):
        '''
        Player should be "player" or "dealer"
        '''

        if player == "player":
            self.playerCards.append(self.deck.pop(0))
        else:
            self.dealerCards.append(self.deck.pop(0))


STATE = BlackJackState()

from gent import GameObject
from gent import Box, TextLine

from typing import Tuple

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
                (i * 24 + 2, 24),
                STATE.playerCards[i]
            ))
        
        for i in range(len(STATE.dealerCards)):
            self.dealerCards.append(Card(
                (i * 24 + 2, 1),
                STATE.dealerCards[i]
            ))

    def _setValues(self):
        '''

        '''

        self.bufferCanvas.backgroundColors.fill(0)

        card: Card
        for card in self.playerCards:
            card.drawOn(self)
        
        for card in self.dealerCards:
            card.drawOn(self)

from gent import Game
def run():

    STATE.deal()
    g = Game(STATE, (180, 40))

    table = Table()
    g.addGameObject(table)

    g.gameLoop()