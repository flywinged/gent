# Copyright Clayton Brown 2019. See LICENSE file.

from gent import Game

from .screen import StartScreen
from .buttons import PlayButton, QuitButton

def setStart(game: Game):
    '''
    Set all the correct game object for the blackjack game start menu
    '''

    # First clear all the object that are currently in the game
    game.clearGameObjects()

    # Now create the necessary start menu info
    startScreen = StartScreen()
    game.addGameObject(startScreen, layer = 0)

    playButton = PlayButton(game)
    game.addGameObject(playButton, layer = 1)
    quitButton = QuitButton(game)
    game.addGameObject(quitButton, layer = 1)

    startScreen.objectHandler.addConnection(playButton, quitButton, "D")
    startScreen.objectHandler.selectObject(playButton)

    game.activeGameObject = startScreen