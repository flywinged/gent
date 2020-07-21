# Copyright Clayton Brown 2019. See LICENSE file.

from gent import GameObject, TextLine, Box

class BlackjackHelp(GameObject):
    '''

    '''

    def __init__(self):
        GameObject.__init__(self, Box(0, 0, 80, 32))
    
    def _setValues(self):
        '''

        '''

        self.bufferCanvas.backgroundColors.fill(120)
        self.bufferCanvas.transparency.fill(40)
