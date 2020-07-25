# Copyright Clayton Brown 2019. See LICENSE file.

from .start import setStart
from .game import setGame

from gent import Game

def initializeScreens(game: Game):
    
    game.addScreen("Start", setStart)
    game.addScreen("Game",  setGame)