# Copyright Clayton Brown 2019. See LICENSE file.

from ...state import CardData

from typing import List, Tuple

from gent import Box
from gent import GameObject
from gent import TextLine

from ...state import STATE

class Controls(GameObject):
    '''
    Display a single card
    '''

    def __init__(self):
        GameObject.__init__(self, Box(0, 14, 54, 5))
    
    def render(self):
        self.bufferCanvas.backgroundColors[:,:] = (60, 15, 90)