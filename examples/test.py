# Copyright Clayton Brown 2019. See LICENSE file.

from gent.game import Game
from gent.game import GameState

def test():

    gs = GameState()
    g = Game(gs, (80, 40))

    g.gameLoop()