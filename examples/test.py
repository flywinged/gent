# Copyright Clayton Brown 2019. See LICENSE file.

from gent import GameState, Game

def test():

    gs = GameState()
    g = Game(gs, (80, 40))

    g.gameLoop()