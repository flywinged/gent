# Copyright Clayton Brown 2019. See LICENSE file.

import os
import sys
import time

import colorama

from typing import Tuple, Dict

from threading import Thread

from ..internal import Event, GameObject, Canvas, timeFunction, GameState
from .getch import EventGetter

import traceback

class Game:
    '''
    Parent class for handling visuals on the canvas.

    Parameters
    ----------
    canvasSize: Tuple of (canvasWidth, canvasHeight)
    '''
            
    class CanvasDrawThread(Thread):
        '''

        '''

        def __init__(self, game: "Game"):
            Thread.__init__(self)

            self.game: Game = game
        
        def run(self):
            
            try:
                while self.game.isActive:

                    # Determine when this loop starts
                    startTime = timeFunction()


                    ##############################
                    # DRAW GAMEOBJECTS ON CANVAS #
                    ##############################

                    # First clear the canvas
                    canvas = self.game.bufferCanvas
                    canvas.clearCanvas()

                    # Draw each gameObject in each layer
                    layerList = sorted(list(self.game.layerToGameObjectIDMap))

                    for layer in layerList:
                        gameObjects = self.game.layerToGameObjectIDMap[layer]
                        for gameObjectID in gameObjects:
                            gameObject = self.game.gameObjectsIDMap[gameObjectID]
                            gameObject.draw(canvas)

                    self.game.switchBuffers()


                    ########################
                    # PRINT WHAT WAS DRAWN #
                    ########################
                    
                    # Print the new screen.
                    if self.game.isDisplayActive:
                        
                        # Move the cursor back to the beginning of the screen
                        print("%s" % colorama.Cursor.POS(), end = "")

                        canvas = self.game.activeCanvas
                        print(canvas.getCanvasText(), end = "")
                    
                    # Now we need to wait the appropriate amount of time before calling the next draw
                    timeLeft = self.game.drawDelay - (timeFunction() - startTime)
                    if timeLeft < 0.005: timeLeft = 0.005 # We never want to fully saturate this thread

                    # Sleep the appropriate amount of time to keep the drawDelay up
                    time.sleep(timeLeft)
                
            except:
                self.game.isActive = False
                print(traceback.format_exc())
    
    class UpdateThread(Thread):
        '''

        '''

        def __init__(self, game: "Game"):
            Thread.__init__(self)

            self.game: Game = game

        def run(self):

            try:

                # As long as the game is active we want to update continuously
                while self.game.isActive:

                    # Update the game state time before any updates are performed
                    self.game.gameState.updateTime()

                    # Then perform any global game updates
                    self.game.update()

                    # Then we want to update every gameObject
                    for gameObjectID in self.game.gameObjectsIDMap:
                        gameObject = self.game.gameObjectsIDMap[gameObjectID]
                        gameObject.update()
                    
                    # Now we need to wait the appropriate amount of time before calling the next update fram
                    timeLeft = self.game.updateDelay - (timeFunction() - self.game.gameState.now)
                    if timeLeft < 0.005: timeLeft = 0.005 # We never want to fully saturate this thread

                    # Sleep the appropriate amount of time to keep the update rate up
                    time.sleep(timeLeft)
                        
            except:
                self.game.isActive = False
                print(traceback.format_exc())

    def __init__(self, gameState: GameState, canvasSize: Tuple[int, int], updateDelay: float = 1 / 60, drawDelay: float = 1 / 60):

        # Initialize the gameState
        self.gameState: GameState = gameState

        # Set the height and width of the game, and then set those values in the terminal
        self.width: int = canvasSize[0]
        self.height: int = canvasSize[1]

        # Resize the terminal game according to the platform
        if sys.platform == "darwin":
            sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=self.height,cols=self.width))
        
        elif sys.platform == "win32":
            os.system("mode con lines=%i cols=%i" % (self.height, self.width))
        
        elif sys.platform == "linux":
            print("\x1b[8;%i;%it" % (self.height, self.width))

        # Assign the frame and update rates
        self.drawDelay: float = drawDelay
        self.updateDelay: float = updateDelay

        # Dictionary of GameObjectIDs assigned to their respective layers
        self.gameObjectIDToLayerMap: Dict[int, int] = {}

        # Dictionary of gameObjectIDs to their corresponding game object
        self.gameObjectsIDMap: Dict[int, GameObject] = {}

        # Dictionary of layers corresponding to all the game objects in that layer
        self.layerToGameObjectIDMap: Dict[int, set] = {}

        # The canvas buffer values. Setting up a double buffer so that drawing and things can happen on a different thread and not interrupt the draw loop.
        self.activeCanvas: Canvas = Canvas(self.width, self.height)
        self.bufferCanvas: Canvas = Canvas(self.width, self.height)

        # Determine what the active gameObject is
        self.rootGameObject: GameObject = None

        # Whether or not the subthreads need to continue
        self.isActive: bool = True
        self.isDisplayActive: bool = True

        # This is for time management purposes
        self.currentTime: float = timeFunction()

        # Create the game Threads
        self.canvasDrawThread: Game.CanvasDrawThread = Game.CanvasDrawThread(self)
        self.updateThread: Game.UpdateThread = Game.UpdateThread(self)

        # Initialize colorama
        colorama.init()
    
    def addGameObject(self, gameObject: GameObject, layer: int = 0):
        '''
        Puts a game object into the game. Handles all the layering and everything.

        Parameters
        ----------
        gameObject: The game object to add to the game. Can be a raw gameObject or any of its children

        layer: This is the layer to add the gameObject to. This should be an integer. Game objects are drawn from smallest layer to largest layer
        '''

        # First match the gameObject to layer map
        self.gameObjectIDToLayerMap[gameObject.ID] = layer

        # Then add the gameObjectID to the layer map
        if layer not in self.layerToGameObjectIDMap:
            self.layerToGameObjectIDMap[layer] = set()

        self.layerToGameObjectIDMap[layer].add(gameObject.ID)

        # Then add the gameObject to the gameObjectMap!
        self.gameObjectsIDMap[gameObject.ID] = gameObject

        return True
    
    def removeGameObject(self, gameObject: GameObject):
        '''
        Removes a gameObject from the game.
        '''

        # Make sure the gameObjectID exists
        if gameObject.ID not in self.gameObjectsIDMap:
            return False

        # First, determine which layer the gameObject is a part of
        layer = self.gameObjectIDToLayerMap[gameObject.ID]

        # Then remove the gameObject from that layer
        self.layerToGameObjectIDMap[layer].remove(gameObject.ID)

        # Then remove the gameObject from the gameObjectMap!
        del self.gameObjectsIDMap[gameObject.ID]

        return True

    def assignGameObjectLayer(self, gameObject: GameObject, newLayer: int):
        '''
        Reassign a gameobject's render layer.
        '''

        self.removeGameObject(gameObject)
        self.addGameObject(gameObject, newLayer)

    def handleEvent(self, event: Event):
        '''
        
        '''

        # Whatever the active game object is, call event handler for it
        if self.rootGameObject:
            self.rootGameObject.handleEvent(event)

    def switchBuffers(self):
        '''
        Flip the active and buffer canvass.
        '''

        self.activeCanvas, self.bufferCanvas = self.bufferCanvas, self.activeCanvas

    def update(self):
        '''
        Virtual function to overwrite by children. Called each loop in the updateLoop
        '''

    def gameLoop(self):
        '''
        Start the game loop.
        '''

        self.canvasDrawThread.start()
        self.updateThread.start()

        # Create the getch object and start an event loop
        G = EventGetter()
        while self.isActive:
            event = G.getEvent()

            # Control C
            if event.keyName == "EXIT":
                self.isActive = False
            
            # Control D
            if event.keyNumber == (4, ):
                self.isDisplayActive = not self.isDisplayActive
            
            # This is for error management. If something breaks, kill the game and print the error
            try:
                self.handleEvent(event)
            except:
                self.isActive = False                    
                print(traceback.format_exc())

        G.getchThread.running = False