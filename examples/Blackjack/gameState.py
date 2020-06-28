# Copyright Clayton Brown 2019. See LICENSE file.

from gent import GameState

from typing import List

from .card import CardData, createDeck

class BlackJackState(GameState):
    '''
    Contains deck info for playing blackjack
    '''

    def __init__(self):
        GameState.__init__(self)

        self.deck: List[CardData] = []

        self.dealerCards: List[CardData] = []
        self.playerCards: List[CardData] = []

        # Who's turn it is
        self.turn: str = "player"
    
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