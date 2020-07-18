# Copyright Clayton Brown 2019. See LICENSE file.


from .gameState import STATE
from .table import Table
from .help import BlackjackHelp

from gent import Game
def run():

    STATE.deal()
    g = Game(STATE, (180, 40))

    g.helpObject = BlackjackHelp()

    table = Table()
    g.addGameObject(table)

    g.gameLoop()