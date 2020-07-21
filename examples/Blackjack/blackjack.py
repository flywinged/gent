# Copyright Clayton Brown 2019. See LICENSE file.

# Main blackjack file. Create the game and starts the menu screen.
from .gameState import STATE
from .table import Table
from .help import BlackjackHelp

from .screens import setStart

from gent import Game
def run():

    STATE.deal()
    g = Game(STATE, (80, 32))

    g.helpObject = BlackjackHelp()

    setStart(g)

    # table = Table()
    # g.addGameObject(table)

    g.gameLoop()