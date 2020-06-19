# Copyright Clayton Brown 2019. See LICENSE file.


from .gameState import STATE
from .table import Table

from gent import Game
def run():

    STATE.deal()
    g = Game(STATE, (180, 40))

    table = Table()
    g.addGameObject(table)

    g.gameLoop()