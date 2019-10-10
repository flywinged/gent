from .event import Event, EVENT_HANDLER
from .box import Box

from .canvas import Canvas

from .event import Event

from typing import Dict, Set

from dataclasses import dataclass     

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

    NEW_OBJECT_ID = 1

    def __init__(self, box: Box, selectionHandler = None, isSelectable: bool = True):

        # Give the game object and ID so that it can be kept track of later
        self.ID: int = GameObject.NEW_OBJECT_ID
        GameObject.NEW_OBJECT_ID += 1

        # Create the real width and height (This is the raw input when the gameObject is created)
        self.realX: int = box.x
        self.realY: int = box.y
        self.realW: int = box.w
        self.realH: int = box.h

        # Whether or not pressing enter on the object will select it
        self.isSelectable: bool = isSelectable

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

        # Set the current selection status
        self.selectionStatus = GameObject.OUTLINED
    
        # Toggle if the gameObject should be draw on the screen or not
        self.drawObject: bool = True

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

        self.setValues()

        x, y, w, h = self.realX + offset[0], self.realY + offset[1], self.realW, self.realH

        destination.characters[x:x + w, y:y + h] = self.activeCanvas.characters
        destination.textColors[x:x + w, y:y + h] = self.activeCanvas.textColors
        destination.backgroundColors[x:x + w, y:y + h] = self.activeCanvas.backgroundColors

    def _handleEvent(self, event: Event): #pylint: disable=unused-argument
        '''
        Allow the gameObject to handle an event internally.

        Parameters
        ----------
        event: Event for the gameObject to handle.
        '''

        # Virtual event handler to be overwritten by all children
        return EVENT_HANDLER.DID_NOT_HANDLE

    def handleEvent(self, event: Event):
        '''
        How the game object should handle events
        '''

        # Initialize to not handling the event
        handlerReturn = EVENT_HANDLER.DID_NOT_HANDLE

        # If there is no object handler, the object handles the event itself
        if self.objectHandler == None:
            if event.keyName == "ESCAPE" or event.keyName == "TAB":
                return EVENT_HANDLER.EXIT

            handlerReturn = self._handleEvent(event)

        # Otherwise, let the object handler handle the event
        else:
            handlerReturn = self.objectHandler.handleEvent(event)

        self._onEvent(event)
        
        return handlerReturn

    def _onEvent(self, event: Event):
        '''
        Is called each time the gameObject captures an event
        '''

        # Virtual function to be overwritten

    def _update(self):
        '''
        Update function to call each frame.
        '''

        # Virtual function to be overwritten by any children which need it

    def update(self):
        if self.objectHandler != None:
            self.objectHandler.update()
        
        self._update()

    def _setValues(self):
        '''
        Update the gameobject values to reflect what has been added.
        '''
        
        # Virtual function to be overwritten by any children which need it

    def _setValuesAfterSelection(self):
        '''
        Update the gameObject values after the selectionHandler has been called
        '''

        # Virtual function to be overwritten by children

    def setValues(self):
        '''
        Handler for gameObject setting its internal values
        '''

        self._setValues()
        
        if self.selectionStatus == self.SELECTED: self.selectionHandler.select()
        elif self.selectionStatus == self.HOVERED: self.selectionHandler.hover()
        elif self.selectionStatus == self.OUTLINED: self.selectionHandler.default()

        self._setValuesAfterSelection()

        self.swapBuffers()
    
    def _onExit(self):
        '''
        When the object handler leaves the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it
    
    def onExit(self):
        self.selectionStatus = self.HOVERED
        self._onExit()
    
    def _onEntry(self):
        '''
        When the object handler selects the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it
    
    def onEntry(self):
        self.selectionStatus = self.SELECTED
        self._onEntry()

        if self.objectHandler != None:
            self.objectHandler.currentGameObject.onHoverEntry()
    
    def _onHoverEntry(self):
        '''
        When the object handler hovers over the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it

    def onHoverEntry(self):
        self.selectionStatus = self.HOVERED
        self._onHoverEntry()
    
    def _onHoverExit(self):
        '''
        When the object handler stops hovering over the gameObject, what should the gameObject do
        '''

        # Virtual function to be overwritten by any children which need it
    
    def onHoverExit(self):
        self.selectionStatus = self.OUTLINED
        self._onHoverExit()


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

    def handleEvent(self, event: Event):

        # If we are selecting an object, we need to determine
        if self.selectingObject:

            # If Escape is pressed, the object handler should return False, indicating the object handler should be broken out of the event loop.
            if event.keyName == "ESCAPE" or event.keyName == "TAB":
                self.currentGameObject.onHoverExit()
                return EVENT_HANDLER.EXIT

            # Determine which game object is in the location determined by the key press
            nextGameObject = None

            # Determine which gameObject to move to if the gameObject is in the connections
            if self.currentGameObject in self.connections:
                if event.keyName == "UP" or event.char == "e":
                    nextGameObject = self.connections[self.currentGameObject].up
                if event.keyName == "DOWN" or event.char == "d":
                    nextGameObject = self.connections[self.currentGameObject].down
                if event.keyName == "LEFT" or event.char == "s":
                    nextGameObject = self.connections[self.currentGameObject].left
                if event.keyName == "RIGHT" or event.char == "f":
                    nextGameObject = self.connections[self.currentGameObject].right
            
            if event.keyName in self.hotKeys:
                nextGameObject = self.hotKeys[event.keyName]
            
            # If the game object isn't none, set it as the current gameObject
            if nextGameObject != None:
                self.selectObject(nextGameObject)
            
            # If return is pressed, we are now switching to object handling mode
            if event.keyName == "RETURN" or event.keyName == "SPACE":
                self.currentGameObject.onEntry()

                if self.currentGameObject.isSelectable:
                    self.selectingObject = False
            
            return EVENT_HANDLER.HANDLED
                    
        # Otherwise, we need to pass the event to the selected gameobject
        if self.currentGameObject.handleEvent(event) == EVENT_HANDLER.EXIT:
            self.currentGameObject.onExit()
            self.currentGameObject.onHoverEntry()

            self.selectingObject = True
            return EVENT_HANDLER.HANDLED

    def selectObject(self, gameObject: GameObject):
        '''
        Unselect whatever the current gameObject is, and select a new gameObject
        '''

        if gameObject in self.gameObjects:

            self.currentGameObject.onHoverExit()
            self.currentGameObject = gameObject
            self.currentGameObject.onHoverEntry()

    def update(self):

        if not self.selectingObject and self.currentGameObject != None:
            self.currentGameObject.update()


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
    
    def _select(self):
        '''
        How to draw the selection indication about the gameObject
        '''

        # Virtual function to be overwritten by children.

    def select(self, override: bool = False):
        if self.drawSelect or override: self._select()
    
    def _hover(self):
        '''
        How to draw the hover indication about the gameObject
        '''

        # Virtual function to be overwritten by children.
    
    def hover(self, override: bool = False):
        if self.drawHover or override: self._hover()
    
    def _default(self):
        '''
        How to draw the default indication about the gameObject
        '''

        # Virtual function to be overwritten by children.
    
    def default(self, override: bool = False):
        if self.drawDefault or override: self._default()