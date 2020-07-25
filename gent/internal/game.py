# Copyright Clayton Brown 2019. See LICENSE file.


from typing import Tuple, Dict, Set
from types import FunctionType

from dataclasses import dataclass

from ..constants import *

import numpy

import os
import sys
import time

import colorama

from threading import Thread

from .box import Box

from .event import Event
from .event import EVENT_HANDLER

from .canvas import Canvas
from .timing import timeFunction
from .gameState import GameState
from .getch import EventGetter

import pynput

import traceback


class GameObject:
    '''
    Base Class for all game objects

    Parameters
    ----------
    box:

    selectionHandler:
    '''

    SELECTED: int = 0
    HOVERED: int = 1
    OUTLINED: int = 2

    NEW_OBJECT_ID: int = 1

    def __init__(self, box: Box, selectionHandler = None, isSelectable: bool = True, isExitable: bool = True, game: "Game" = None):

        # Game reference. This is automatically set with the gameObject is added to the game
        self.game: Game = game

        # Give the game object and ID so that it can be kept track of later
        self.ID: int = int(GameObject.NEW_OBJECT_ID)
        GameObject.NEW_OBJECT_ID += 1

        # Create the real width and height (This is the raw input when the gameObject is created)
        self.realX: int = box.x
        self.realY: int = box.y
        self.realW: int = box.w
        self.realH: int = box.h

        # Whether or not pressing enter on the object will select it
        self.isSelectable: bool = isSelectable

        # Whether or not the user can press EXIT to leave the object
        #   Usually this is set to false for managing top level game objects.
        self.exitable: bool = isExitable

        # Initialize the object handler
        self.objectHandler: ObjectHandler = None

        # Create the usable parameters for the object (These have been adjusted by the handler style)
        self.x: int = box.x
        self.y: int = box.y
        self.w: int = box.w
        self.h: int = box.h
        self.xOffset: int = 0
        self.yOffset: int = 0

        # Initialize the selection handler
        if selectionHandler == None:
            selectionHandler = Selection()
        self.selectionHandler: Selection = selectionHandler
        self.selectionHandler.linkGameObject(self)

        # Create the visuals for gameObjects
        self.activeCanvas: Canvas = Canvas(self.realW, self.realH)
        self.bufferCanvas: Canvas = Canvas(self.realW, self.realH)

        # Whether or not the object will use transparency values
        self.useTransparency: bool = False

        # If hide is set to true, it won't be drawn
        self.hide: bool = False

        # Set the current selection status
        self.selectionStatus = GameObject.OUTLINED

        # The containing objectHandler (To be set upon addition to an objectHandler)
        self.parentObjectHandler: ObjectHandler = None

    def __hash__(self):
        return self.ID

    def addObjectHandler(self):
        '''
        Attaches an object handler to the gameObject. Also attaches the gameObject to th objectHandler
        '''

        self.objectHandler = ObjectHandler(self)

    def swapBuffers(self):
        '''
        Flip the active and buffer canvases
        '''

        self.activeCanvas, self.bufferCanvas = self.bufferCanvas, self.activeCanvas

    def getOffset(self):
        return (self.xOffset, self.yOffset)

    def drawOn(self, gameObject: "GameObject"):
        '''
        Bundles the draw call so you dont have to worry about getting the offset
        '''

        self.draw(gameObject.bufferCanvas, gameObject.getOffset())

    def draw(self, destination: Canvas, offset = (0, 0)):
        '''
        Draw the gameObject onto a canvas

        Parameters
        ----------
        destination: The canvas or gameObject to draw on
        '''

        # Don't do anything if the object is hidden
        if self.hide: return

        self._setValues()

        x, y, w, h = self.realX + offset[0], self.realY + offset[1], self.realW, self.realH

        # If transparency is enabled, we need to do some extra math when drawing.
        if self.useTransparency:

            # If the transparency value is greater than 50% (126 on a scale of 255),
            #   then we want to copy the new text.
            textUpdates = numpy.where(self.activeCanvas.transparency > 126)
            destinationX = numpy.array(textUpdates[0]) + x
            destinationY = numpy.array(textUpdates[1]) + y

            destination.characters[destinationX, destinationY] = self.activeCanvas.characters[textUpdates]

            # Then we apply transparencies to the background and text colors.
            destination.backgroundColors[x:x + w, y:y + h] = (
                destination.backgroundColors[x:x + w, y:y + h].astype(numpy.float32) * numpy.expand_dims(1.0 - self.activeCanvas.transparency.astype(numpy.float32) / 255, 2) +
                self.activeCanvas.backgroundColors.astype(numpy.float32) * numpy.expand_dims(self.activeCanvas.transparency.astype(numpy.float32) / 255, 2)
            ).astype(numpy.uint8)

            destination.textColors[x:x + w, y:y + h] = (
                destination.textColors[x:x + w, y:y + h].astype(numpy.float32) * numpy.expand_dims(1.0 - self.activeCanvas.transparency.astype(numpy.float32) / 255, 2) +
                self.activeCanvas.textColors.astype(numpy.float32) * numpy.expand_dims(self.activeCanvas.transparency.astype(numpy.float32) / 255, 2)
            ).astype(numpy.uint8)
            
        else:
            destination.characters[x:x + w, y:y + h] = self.activeCanvas.characters
            destination.textColors[x:x + w, y:y + h] = self.activeCanvas.textColors
            destination.backgroundColors[x:x + w, y:y + h] = self.activeCanvas.backgroundColors

    def handleEvent(self, event: Event): #pylint: disable=unused-argument
        '''
        Allow the gameObject to handle an event internally.

        Parameters
        ----------
        event: Event for the gameObject to handle.
        '''

        # Virtual event handler to be overwritten by all children
        return EVENT_HANDLER.DID_NOT_HANDLE

    def _handleEvent(self, event: Event):
        '''
        How the game object should handle events
        '''

        # Initialize to not handling the event
        handlerReturn = EVENT_HANDLER.DID_NOT_HANDLE

        # If there is no object handler, the object handles the event itself
        if self.objectHandler == None:
            if self.exitable and event.keyName in CONNECTION_BACK:
                return EVENT_HANDLER.EXIT

            handlerReturn = self.handleEvent(event)

        # Otherwise, let the object handler handle the event
        else:
            handlerReturn = self.objectHandler._handleEvent(event)

        # After the object handler tackles the event, 
        self.onEvent(event)
        
        return handlerReturn

    def onEvent(self, event: Event):
        '''
        Is called each time the gameObject captures an event
        '''

        # Virtual function to be overwritten

    def update(self):
        '''
        Update function to call each frame.
        '''

        # Virtual function to be overwritten by any children which need it

    def _update(self):
        if self.objectHandler != None:
            self.objectHandler._update()
        
        self.update()

    def setValues(self):
        '''
        Update the gameobject values to reflect what has been added.

        Should draw to self.bufferCanvas
        '''
        
        # Virtual function to be overwritten by any children which need it

    def setValuesAfterSelection(self):
        '''
        Update the gameObject values after the selectionHandler has been called
        '''

        # Virtual function to be overwritten by children

    def _setValues(self):
        '''
        Handler for gameObject setting its internal values
        '''

        self.bufferCanvas.clearCanvas()

        self.setValues()
        
        if self.selectionStatus == self.SELECTED: self.selectionHandler._select()
        elif self.selectionStatus == self.HOVERED: self.selectionHandler._hover()
        elif self.selectionStatus == self.OUTLINED: self.selectionHandler._default()

        self.setValuesAfterSelection()

        self.swapBuffers()
    
    def onExit(self):
        '''
        When the object handler leaves the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it
    
    def _onExit(self):
        self.selectionStatus = self.HOVERED
        self.onExit()

    def onPress(self):
        '''
        Called when the "enter" key is pressed on the game object from a parent.
        '''

        # Virtual Function to be overwritten by children which use it.
    
    def onEntry(self):
        '''
        When the object handler selects the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it
    
    def _onEntry(self):
        self.selectionStatus = self.SELECTED
        self.onEntry()

        if self.objectHandler != None:
            self.objectHandler.currentGameObject._onHoverEntry()
    
    def onHoverEntry(self):
        '''
        When the object handler hovers over the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it

    def _onHoverEntry(self):
        self.selectionStatus = self.HOVERED
        self.onHoverEntry()
    
    def onHoverExit(self):
        '''
        When the object handler stops hovering over the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it
    
    def _onHoverExit(self):
        self.selectionStatus = self.OUTLINED
        self.onHoverExit()


##################
# OBJECT HANDLER #
##################

@dataclass
class Node:

    up: GameObject = None
    down: GameObject = None
    left: GameObject = None
    right: GameObject = None

    def clear(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None

class ObjectHandler:
    '''

    '''

    def __init__(self, gameObject: GameObject):

        # The gameObject the object handler is attached to
        self.gameObject: GameObject = gameObject

        # Each node
        self.gameObjects: Set[GameObject] = set()
        self.connections: Dict[GameObject, Node] = {}
        self.hotKeys: Dict[str, GameObject] = {}
        self.currentGameObject: GameObject = None

        # Whether or not the object handler is currently selecting an object, or handling an object
        self.selectingObject: bool = True

    def addConnection(self, gameObject1: GameObject, gameObject2: GameObject, connectionType: str):
        '''
        Adds a connection between two gameobjects to the ObjectHandler. Will add the gameobjects to the ObjectHandler if they aren't already there

        Parameters
        ----------
        gameObject1/2: The two game objects to connect

        connectionType: "U", "D", "L", "R" (up, down, left, or right) This is the relation of gameObject2 to gameObject1.
        '''

        # Check if either game object is in the current object handler dictionary.
        if gameObject1 not in self.connections:
            self.connections[gameObject1] = Node()
        if gameObject2 not in self.connections:
            self.connections[gameObject2] = Node()
        
        # Add the appropriate connections
        if connectionType == "U":
            self.connections[gameObject1].up = gameObject2
            self.connections[gameObject2].down = gameObject1
        elif connectionType == "D":
            self.connections[gameObject1].down = gameObject2
            self.connections[gameObject2].up = gameObject1
        elif connectionType == "L":
            self.connections[gameObject1].left = gameObject2
            self.connections[gameObject2].right = gameObject1
        elif connectionType == "R":
            self.connections[gameObject1].right = gameObject2
            self.connections[gameObject2].left = gameObject1
        else:
            raise Exception("No Connection Type Provided")
            
        # Add the gameobjects to the gameObject set
        self.gameObjects.add(gameObject1)
        gameObject1.parentObjectHandler = self

        self.gameObjects.add(gameObject2)
        gameObject2.parentObjectHandler = self
    
    def clearConnections(self):
        '''
        Use with caution as things could seriously break if the connections aren't immediately reinstated
        '''

        for gameObject in self.connections:
            self.connections[gameObject].clear()

    def addHotKey(self, gameObject: GameObject, hotKey: str):
        '''
        Adds a hotKey to accessing a specific gameObject. You can only do this if the gameObject has already been added to the map

        Parameters
        ----------
        gameObject: The gameObject to attach a hotkey to

        kotKey: event.keyName for the hotKey
        '''

        # Add the hotkey to the gameObject and add the gameObject to the set
        self.hotKeys[hotKey] = gameObject
        self.gameObjects.add(gameObject)
        gameObject.parentObjectHandler = self

    def _handleEvent(self, event: Event):

        # Can't do anything if there is not an active object
        if self.currentGameObject is None:
            
            if event.keyName in CONNECTION_BACK and self.gameObject.exitable:
                self.gameObject.onExit()
            
            if event.keyName in self.hotKeys:
                nextGameObject = self.hotKeys[event.keyName]

        # If we are selecting an object, we need to determine
        elif self.selectingObject:

            # If Escape is pressed, the object handler should return False, indicating the object handler should be broken out of the event loop.
            if event.keyName in CONNECTION_BACK and self.gameObject.exitable:
                self.currentGameObject._onHoverExit()
                return EVENT_HANDLER.EXIT

            # Determine which game object is in the location determined by the key press
            nextGameObject = None

            # Determine which gameObject to move to if the gameObject is in the connections
            if self.currentGameObject in self.connections:
                if event.keyName in CONNECTION_UP:
                    nextGameObject = self.connections[self.currentGameObject].up
                if event.keyName in CONNECTION_DOWN:
                    nextGameObject = self.connections[self.currentGameObject].down
                if event.keyName in CONNECTION_LEFT:
                    nextGameObject = self.connections[self.currentGameObject].left
                if event.keyName in CONNECTION_RIGHT:
                    nextGameObject = self.connections[self.currentGameObject].right
            
            if event.keyName in self.hotKeys:
                nextGameObject = self.hotKeys[event.keyName]
            
            # If the game object isn't none, set it as the current gameObject
            if nextGameObject != None:
                self.selectObject(nextGameObject)
            
            # If return is pressed, we are now switching to object handling mode
            if event.keyName in CONNECTION_ENTER:
                self.currentGameObject.onPress()
                if self.currentGameObject.isSelectable:
                    self.currentGameObject._onEntry()
                    self.selectingObject = False
                else:
                    self.currentGameObject.onEntry()
                    
        # Otherwise, we need to pass the event to the selected gameobject
        elif self.currentGameObject._handleEvent(event) == EVENT_HANDLER.EXIT:
            self.currentGameObject._onExit()
            self.currentGameObject._onHoverEntry()

            self.selectingObject = True
            return EVENT_HANDLER.HANDLED
        
        return EVENT_HANDLER.DID_NOT_HANDLE

    def selectObject(self, gameObject: GameObject):
        '''
        Unselect whatever the current gameObject is, and select a new gameObject
        '''

        if gameObject in self.gameObjects:

            if self.currentGameObject is not None:
                self.currentGameObject._onHoverExit()
            
            self.currentGameObject = gameObject
            self.currentGameObject._onHoverEntry()

    def _update(self):

        if not self.selectingObject and self.currentGameObject != None:
            self.currentGameObject._update()


#############
# SELECTION #
#############

class Selection:
    '''
    Parent class for handling selection statuses
    '''

    def __init__(self, drawSelect: bool = True, drawHover: bool = True, drawDefault: bool = True):
        self.gameObject: GameObject = None
        self.drawSelect: bool = drawSelect
        self.drawHover: bool = drawHover
        self.drawDefault: bool = drawDefault

    def setDraw(self, default: bool, hover: bool, select: bool):
        self.drawSelect = select
        self.drawHover = hover
        self.drawDefault = default

    def linkGameObject(self, gameObject: GameObject):
        self.gameObject = gameObject
        self.setBoxes()

    def setBoxes(self):
        '''
        Overwrite the x, y, w, h, xOffset, and yOffset of the gameobject
        '''

        # Virtual function to be overwritten by children.
    
    def select(self):
        '''
        How to draw the selection indication about the gameObject
        '''

        # Virtual function to be overwritten by children.

    def _select(self, override: bool = False):
        if self.drawSelect or override: self.select()
    
    def hover(self):
        '''
        How to draw the hover indication about the gameObject
        '''

        # Virtual function to be overwritten by children.
    
    def _hover(self, override: bool = False):
        if self.drawHover or override: self.hover()
    
    def default(self):
        '''
        How to draw the default indication about the gameObject
        '''

        # Virtual function to be overwritten by children.
    
    def _default(self, override: bool = False):
        if self.drawDefault or override: self.default()



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
                        for gameObjectID in list(gameObjects):

                            gameObject: GameObject
                            try:
                                gameObject = self.game.gameObjectsIDMap[gameObjectID]
                            except KeyError:
                                continue
                            gameObject.draw(canvas)
                    
                    if self.game.helpActive:
                        self.game.helpObject.draw(canvas)

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
                self.game.quit()
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
                    self.game._update()

                    # Then we want to update every gameObject
                    for gameObjectID in list(self.game.gameObjectsIDMap):

                        gameObject: GameObject
                        try:
                            gameObject = self.game.gameObjectsIDMap[gameObjectID]
                        except KeyError:
                            continue
                        
                        gameObject._update()
                    
                    # Now we need to wait the appropriate amount of time before calling the next update fram
                    timeLeft = self.game.updateDelay - (timeFunction() - self.game.gameState.now)
                    if timeLeft < 0.005: timeLeft = 0.005 # We never want to fully saturate this thread

                    # Sleep the appropriate amount of time to keep the update rate up
                    time.sleep(timeLeft)
                        
            except:
                self.game.quit()
                print(traceback.format_exc())

    def __init__(self, gameState: GameState, canvasSize: Tuple[int, int], updateDelay: float = 1 / 60, drawDelay: float = 1 / 60):

        # Initialize the gameState
        self.gameState: GameState = gameState

        # Object used to manage event thread
        self.eventGetter: EventGetter = EventGetter()

        # Dictionary containing all the screens for this game and the respective functions to get there
        self.screens: Dict[str, FunctionType] = {}

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
        self.activeGameObject: GameObject = None

        # Whatever the active help object is
        self.helpObject: GameObject = None
        self.helpActive: bool = False

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

        # Before adding the gameObject, attach the game as a reference
        gameObject.game = self

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

    def clearGameObjects(self):
        '''
        Delete all game objects currently in the game.
        '''

        for gameObjectID in list(self.gameObjectsIDMap):
            self.removeGameObject(self.gameObjectsIDMap[gameObjectID])

    def assignGameObjectLayer(self, gameObject: GameObject, newLayer: int):
        '''
        Reassign a gameobject's render layer.
        '''

        self.removeGameObject(gameObject)
        self.addGameObject(gameObject, newLayer)

    def _handleEvent(self, event: Event):
        '''
        
        '''

        # First check to see if the use requested the help window to open or close.
        if event.keyName in HOTKEY_OPEN_HELP and self.helpObject is not None:
            if self.helpActive:
                self.removeGameObject(self.helpObject)
            else:
                self.addGameObject(self.helpObject)
            self.helpActive = not self.helpActive

        # If the help window is active, it captures the event.
        elif self.helpObject in self.gameObjectsIDMap:
            self.helpObject._handleEvent(event)

        # Otherwise, the active game object will handle it.
        elif self.activeGameObject:
            self.activeGameObject._handleEvent(event)

    def switchBuffers(self):
        '''
        Flip the active and buffer canvass.
        '''

        self.activeCanvas, self.bufferCanvas = self.bufferCanvas, self.activeCanvas

    def _update(self):
        '''
        Virtual function to overwrite by children. Called each loop in the updateLoop
        '''
    
    def addScreen(self, screenName: str, function: FunctionType):
        '''
        Adds to a dictionary a function which will reset the game to a specific value.
        The function must have a game obbject as its first and only argument.
        '''

        if callable(function):
            self.screens[screenName] = function
        else:
            raise "Function parameter is not a callable."

    
    def goToScreen(self, screenName: str):
        '''
        Calls the saved screen function by passing in self.
        '''

        if screenName in self.screens:
            self.clearGameObjects()
            self.screens[screenName](self)
        else:
            raise "Screen " + screenName + " not understood."
    
    def quit(self):
        '''
        Quits the game by turning off al the threads and then returning
        '''

        self.isActive = False
        self.isDisplayActive = False

        while self.canvasDrawThread.isAlive(): time.sleep(0.05)
        while self.updateThread.isAlive(): time.sleep(0.05)

        # Clsoe the getch thread
        self.eventGetter.getchThread.running = False
        print("Successfully Quit Game")
        print("\r", end = "")

        # Simulate a keypress to end the getch thread
        keyboard = pynput.keyboard.Controller()
        keyboard.press("a")

    def gameLoop(self):
        '''
        Start the game loop.
        '''

        self.canvasDrawThread.start()
        self.updateThread.start()

        while self.isActive:
            event = self.eventGetter.getEvent()

            # Control C
            if event.keyName == "EXIT":
                self.quit()
            
            # Control D
            if event.keyNumber == (4, ):
                self.isDisplayActive = not self.isDisplayActive
            
            # This is for error management. If something breaks, kill the game and print the error
            try:
                self._handleEvent(event)
            except:
                self.quit()                    
                print(traceback.format_exc())

