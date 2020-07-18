# Copyright Clayton Brown 2019. See LICENSE file.

from gent import GameObject, TextLine, Box

class BlackjackHelp(GameObject):
    '''

    '''

    def __init__(self):
        GameObject.__init__(self, Box(20, 5, 140, 30))
    
    def _setValues(self):
        '''

        '''

        self.bufferCanvas.backgroundColors.fill(125)
