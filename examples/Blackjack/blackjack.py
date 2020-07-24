# Copyright Clayton Brown 2019. See LICENSE file.

# Main blackjack file. Create the game and starts the menu screen.
from .gameState import STATE
from .table import Table
from .help import BlackjackHelp

from .screens import setStart, setGame

from gent import Game
def run():

    STATE.deal()
    g = Game(STATE, (80, 32))

    g.helpObject = BlackjackHelp()

    g.addScreen("Start", setStart)
    g.addScreen("Game", setGame)

    g.goToScreen("Start")
    # table = Table()
    # g.addGameObject(table)

    g.gameLoop()