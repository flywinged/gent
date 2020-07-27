# Copyright Clayton Brown 2019. See LICENSE file.

# Main blackjack file. Create the game and starts the menu screen.
from .state import STATE

from .screens import initializeScreens

from gent import Game

def run():

    # Initialize the state
    STATE.deal()

    # Create the game object
    g = Game(STATE, (54, 19))

    # Add all the screens to the game
    initializeScreens(g)

    # Start the game on the start screen
    g.goToScreen("Start")
    g.gameLoop()