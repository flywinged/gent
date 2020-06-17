import os
import sys
import time

import colorama

from typing import Tuple, Dict

from threading import Thread

from ..internal import Event, GameObject, Canvas, timeFunction
from .getch import EventGetter

import traceback

class Window:
    '''
    Parent class for handling visuals on the canvas.

    Parameters
    ----------
    canvasSize: Tuple of (canvasWidth, canvasHeight)
    '''

    class CanvasUpdateThread(Thread):
        '''
        The canvasUpdateThread handles all the repetitive drawing that needs to happen and will keep the window canvass constantly updated.
        '''

        def __init__(self, window: "Window"):
            Thread.__init__(self)

            self.window: Window = window
        
        def run(self):

            try:
                while self.window.isActive:
                    
                    # First clear the canvas
                    canvas = self.window.bufferCanvas
                    canvas.clearCanvas()

                    # Draw each gameObject in each layer
                    layerList = sorted(list(self.window.layerToGameObjectIDMap))

                    for layer in layerList:
                        gameObjects = self.window.layerToGameObjectIDMap[layer]
                        for gameObjectID in gameObjects:
                            gameObject = self.window.gameObjectsIDMap[gameObjectID]

                            if gameObject.drawObject:
                                gameObject.draw(canvas)

                    self.window.switchBuffers()

                    time.sleep(.02)

            except:
                self.window.isActive = False
                print(traceback.format_exc())
            
    class CanvasDrawThread(Thread):
        '''

        '''

        def __init__(self, window: "Window"):
            Thread.__init__(self)

            self.window: Window = window
        
        def run(self):
            
            try:
                while self.window.isActive:

                    # Move the cursor back to the beginning of the screen
                    print("%s" % colorama.Cursor.POS(), end = "")
                    
                    # Print the new screen.
                    if self.window.isDisplayActive:
                        canvas = self.window.activeCanvas
                        print(canvas.getCanvasText(), end = "")
                    
                    # Slight delay to prevent overuse of the thread.
                    time.sleep(0.005)

            except:
                self.window.isActive = False
                print(traceback.format_exc())
    
    class UpdateThread(Thread):
        '''

        '''

        def __init__(self, window: "Window"):
            Thread.__init__(self)

            self.window: Window = window

        def run(self):

            try:
                while self.window.isActive:

                    time.sleep(.02)
                    self.window.update()

                    for gameObjectID in self.window.gameObjectsIDMap:
                        gameObject = self.window.gameObjectsIDMap[gameObjectID]
                        gameObject.update()
                        
            except:
                self.window.isActive = False
                print(traceback.format_exc())

    def __init__(self, canvasSize: Tuple[int, int], frameRate: int = 1):

        # Set the height and width of the window, and then set those values in the terminal
        self.width: int = canvasSize[0]
        self.height: int = canvasSize[1]

        # Resize the terminal window according to the platform
        if sys.platform == "darwin":
            sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=self.height,cols=self.width))
        
        elif sys.platform == "win32":
            os.system("mode con lines=%i cols=%i" % (self.height, self.width))
        
        elif sys.platform == "linux":
            print("\x1b[8;%i;%it" % (self.height, self.width))

        # Assign the framerate
        self.frameRate: int = frameRate

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

        # Create the canvas Threads
        self.canvasUpdateThread: Window.CanvasUpdateThread = Window.CanvasUpdateThread(self)
        self.canvasDrawThread: Window.CanvasDrawThread = Window.CanvasDrawThread(self)
        self.updateThread: Window.UpdateThread = Window.UpdateThread(self)

        # Initialize colorama
        colorama.init()
    
    def addGameObject(self, gameObject: GameObject, layer: int = 0):
        '''
        Puts a game object into the window. Handles all the layering and everything.

        Parameters
        ----------
        gameObject: The game object to add to the window. Can be a raw gameObject or any of its children

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
        Removes a gameObject from the window.
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

        # self.eventThread.start()
        self.canvasUpdateThread.start()
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
            
            # This is for error management. If something breaks, kill the window and print the error
            try:
                self.handleEvent(event)
            except:
                self.isActive = False                    
                print(traceback.format_exc())

        G.getchThread.running = False