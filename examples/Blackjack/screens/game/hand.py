# Copyright Clayton Brown 2019. See LICENSE file.

from ...state import CardData

from typing import List

from gent import Box
from gent import GameObject
from gent import TextLine

class Hand(GameObject):
    '''
    The start screen contains the blackjack background image and user options.
    '''

    def __init__(self, box: Box, cardList: List[CardData]):
        GameObject.__init__(self, box)

        self.cardList: List[CardData] = cardList
        
        self.cardObjects: List[TextLine] = []
        for y in range(self.h):
            textBox = Box(0, y, self.w, 1)
            self.cardObjects.append(TextLine(textBox, "", (255, 255, 255), (20, 20, 20)))
    
    def setValues(self):
        for y in range(len(self.cardList)):
            data = self.cardList[y]
            self.cardObjects[y].text = data.name + " of " + data.suit
            self.cardObjects[y].drawOn(self)