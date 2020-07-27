# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Game

from .screen import GameScreen

from ...state import STATE

def setGame(game: Game):
    '''
    Set all the correct game object for the blackjack game start menu
    '''

    STATE.deal()

    # Now create the necessary start menu info
    gameScreen = GameScreen(game)
    game.addGameObject(gameScreen, layer = 0)

    game.activeGameObject = gameScreen