# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Game

from .screen import StartScreen

def setStart(game: Game):
    '''
    Set all the correct game object for the blackjack game start menu
    '''

    # First clear all the object that are currently in the game
    game.clearGameObjects()

    # Now create the necessary start menu info
    startScreen = StartScreen()
    game.addGameObject(startScreen)
    game.activeGameObject = startScreen