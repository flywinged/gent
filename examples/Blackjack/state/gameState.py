# Copyright Clayton Brown 2019. See LICENSE file.

from gent import GameState

from typing import List

from .deck import CardData, Deck

class BlackJackState(GameState):
    '''
    Contains deck info for playing blackjack
    '''

    def __init__(self):
        GameState.__init__(self)

        self.deck: Deck = Deck()

        self.dealerCards: List[CardData] = []
        self.playerCards: List[CardData] = []

        self.playerCardTotal: int = 0
        self.dealerCardTotal: int = 0

        # Who's turn it is
        self.turn: str = "player"
    
    def deal(self):

        self.deck.reset()
        self.deck.shuffle()

        self.playerCards = []
        self.dealerCards = []

        # Deal the player and the dealer two cards.
        self.playerCards.append(self.deck.cards.pop(0))
        self.dealerCards.append(self.deck.cards.pop(0))
        self.playerCards.append(self.deck.cards.pop(0))
        self.dealerCards.append(self.deck.cards.pop(0))

        self.determineTotals()

    def determineTotals(self):

        # For the player
        aces = 0
        self.playerCardTotal = 0
        for card in self.playerCards:
            card: CardData

            if card.name == "Ace":
                aces += 1
                self.playerCardTotal += 11
            
            elif card.value >= 10:
                self.playerCardTotal += 10
            
            else: 
                self.playerCardTotal += card.value
        
        while self.playerCardTotal > 21 and aces > 0:
            self.playerCardTotal -= 10
            aces -= 1


        # For the dealer
        aces = 0
        self.dealerCardTotal = 0
        for card in self.dealerCards:
            card: CardData

            if card.name == "Ace":
                aces += 1
                self.dealerCardTotal += 11
            
            elif card.value >= 10:
                self.dealerCardTotal += 10
            
            else: 
                self.dealerCardTotal += card.value
        
        while self.dealerCardTotal > 21 and aces > 0:
            self.dealerCardTotal -= 10
            aces -= 1

    def hit(self, player: str):
        '''
        Player should be "player" or "dealer"
        '''

        if player == "player":
            self.playerCards.append(self.deck.cards.pop(0))
        else:
            self.dealerCards.append(self.deck.cards.pop(0))
        
        self.determineTotals()


STATE = BlackJackState()