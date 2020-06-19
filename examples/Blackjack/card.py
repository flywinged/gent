# Copyright Clayton Brown 2019. See LICENSE file.

from dataclasses import dataclass
import random

from typing import List, Tuple

from gent import GameObject, Box, TextLine, loadPNG

@dataclass
class CardData:

    value: int
    name:  str
    suit:  str

cardBack, _ = loadPNG("examples/Blackjack/resources/card-back.png", (20, 15))
cardHeart, _ = loadPNG("examples/Blackjack/resources/card-heart.png", (20, 15))
cardDiamond, _ = loadPNG("examples/Blackjack/resources/card-diamond.png", (20, 15))
cardSpade, _ = loadPNG("examples/Blackjack/resources/card-spade.png", (20, 15))
cardClub, _ = loadPNG("examples/Blackjack/resources/card-club.png", (20, 15))

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
        GameObject.__init__(self, Box(position[0], position[1], 20, 16))

        self.data: CardData = cardData

        self.cardName: TextLine = TextLine(
            Box(0, 0, 20, 1),
            self.data.name + " Of " + self.data.suit,
            (225, 225, 225),
            (0, 0, 0),
            justify="C"
        )

        self.state: str = "visible"
    
    def _setValues(self):
        '''

        '''

        if self.state == "visible":
            self.cardName.drawOn(self)

            # Draw the suit of the card
            cardBackground = cardHeart
            if self.data.suit == "Diamonds":
                cardBackground = cardDiamond
            elif self.data.suit == "Clubs":
                cardBackground = cardClub
            elif self.data.suit == "Spades":
                cardBackground = cardSpade

            self.bufferCanvas.backgroundColors[:,1:,:] = cardBackground[:,:,:]
        
        else:

            # Draw some patern on the back of the card
            self.bufferCanvas.backgroundColors[:,1:,:] = cardBack[:,:,:]