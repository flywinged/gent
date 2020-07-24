# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Box
from gent import TextLine
from gent import loadPNG
from gent import Game
from gent import Selection_Fill

class PlayButton(TextLine):
    '''
    Simple button which displays "Play" on the main start screen. When pressed, does stuff.
    '''

    def __init__(self, game: Game):

        TextLine.__init__(
            self,
            Box(30, 14, 20, 1),
            "Start",
            (255, 255, 255),
            (0, 0, 0),
            justify="C",
            isSelectable=True,
            game=game,
            selectionHandler=Selection_Fill(defaultColor=(60, 15, 90))
        )

class QuitButton(TextLine):
    '''
    Simple button which displays "Play" on the main start screen. When pressed, does stuff.
    '''

    def __init__(self, game: Game):
        TextLine.__init__(
            self,
            Box(30, 15, 20, 1),
            "Quit",
            (255, 255, 255),
            (0, 0, 0),
            justify="C",
            isSelectable=True,
            game=game,
            selectionHandler=Selection_Fill(defaultColor=(60, 15, 90))
        )

        self.game: Game = Game
    
    def onPress(self):

        self.game.quit()