from ..internal import GameObject, Box, Selection_Fill, Event

from .textBox import TextBox
from .textLine import TextLine

from typing import List, Tuple

class BaseSelectorObject(GameObject):
    '''
    Base Object for selector objects
    '''

    def __init__(self, box: Box, gridPosition: Tuple[int, int], **kwargs):
        GameObject.__init__(self, box, isSelectable = False, **kwargs)
        self.selectionHandler.setDraw(False, True, False)

        # Whether or not the selector text has been selected (Used for display purposes)
        self.isSelected: bool = False

        # The position of the SelectorText object in the grid
        self.gridPosition: Tuple[int, int] = gridPosition

        # Whether or not this selectorObject has data
        self.hasData: bool = False
    
    def _onEntry(self):
        '''
        When enter is pressed on the object, the object should toggle whether or not it has been selected.
        '''

        self.isSelected = not self.isSelected
        if not self.isSelected: self.selectionStatus = self.HOVERED

    def _setValuesAfterSelection(self):
        '''
        Make sure the SelectorText draws the correct selection.
        '''

        if self.isSelected: self.selectionHandler.select(override = True)
    
    def updateSelectorObject(self, data):
        '''
        Set all the values you need for selector objects
        '''

        # Virtual Function to overwrite by children
    
    def resetSelectorObject(self):
        '''
        Set all objects to whatever their default should be when no data is shown
        '''

        # Cirtual function to overwrite

class DefaultSelectorObject(BaseSelectorObject):
    '''
    A wrapper for TextBox which
    '''

    def __init__(self, box: Box, gridPosition: Tuple[int, int], **kwargs):
        BaseSelectorObject.__init__(self, box, gridPosition, selectionHandler = Selection_Fill(), **kwargs)
        
        self.textBox: TextBox = TextBox(Box(0, 0, self.w, self.h), "", (255, 255, 255), (0, 0, 0))
    
    def _setValues(self):
        self.textBox.drawOn(self)
    
    def updateSelectorObject(self, data):
        self.textBox.text = data
    
    def resetSelectorObject(self):
        self.textBox.text = ""

class Selector(GameObject):
    '''
    The Selector object handles a grid of choices. There is a custom SelectorText object which is just a wrapper for the textBox object.

    Parameters
    ----------
    box: Position of the Selector

    dimensions: The dimensions of each element of the Selector. Each axis must be divisible by the width of the box.

    elements: List of elements the selector contains

    maxSelections: The maximum number of things which can be selected at any given time.
    '''

    def __init__(self, box: Box, dimensions: Tuple[int, int], elements: List[str], SelectorObject: BaseSelectorObject = DefaultSelectorObject, maxSelections: int = 1, paged: bool = False, **kwargs):
        GameObject.__init__(self, box, selectionHandler = Selection_Fill(drawSelect = False, drawDefault = False), **kwargs)

        self.paged: bool = paged

        # Make sure the dimensions match the width and height
        if self.w % dimensions[0] != 0:
            raise Exception("X Direction doesn't divide evenly")
        if (self.h - 1) % dimensions[1] != 0 and self.paged:
            raise Exception("Y Direction doesn't divide evenly")
        if self.h % dimensions[1] != 0 and not self.paged:
            raise Exception("Y Direction doesn't divide evenly")

        # Set the attributes passed in
        self.dimensions: Tuple[int, int] = dimensions
        self.elements: List = elements
        self.maxSelections: int = maxSelections

        # List of the previous selections made by the user, in order of selection
        self.selectedGridPositions: List[Tuple[int, int]] = []

        # Determine the number of textBoxes in each direction
        if self.paged:
            self.gridDimensions: Tuple[int, int] = (self.w // self.dimensions[0], (self.h - 1) // self.dimensions[1])
        else:
            self.gridDimensions: Tuple[int, int] = (self.w // self.dimensions[0], self.h // self.dimensions[1])

        # Variables concerning which page is currently being displayed
        self.page: int = 1
        self.elementsPerPage: int = self.gridDimensions[0] * self.gridDimensions[1]
        self.maxPages: int = (len(self.elements) // self.elementsPerPage) + 1

        # Create all the SelectorText objects
        self.selectorGrid: List[List[SelectorObject]] = []
        for j in range(self.gridDimensions[1]):

            # Populate each row with selectorTextObjects
            row = []
            for i in range(self.gridDimensions[0]):
                box = Box(i * self.dimensions[0], j * self.dimensions[1], self.dimensions[0], self.dimensions[1])
                selectorText = SelectorObject(box, (i, j))
                row.append(selectorText)
            
            # Add that row to the selectorTextGrid
            self.selectorGrid.append(row)
        
        # Create the page display
        if self.paged:
            self.pageText: TextLine = TextLine(
                Box(0, self.h - 1, self.w, 1),
                "Page %i/%i" % (self.page, self.maxPages),
                (255, 255, 255),
                (0, 0, 0),
                justify = "R"
            )

        # Create the object handler and set the initial gameObject to the element in the topLeft
        self.addObjectHandler()
        self.objectHandler.currentGameObject = self.selectorGrid[0][0]

        # Update the text in each selectorTextObject
        self.updateSelectorObjects(self.elements)

    def updateSelectorObjects(self, elements: List = None):
        '''
        Given a list of elements, set all the SelectorText Objects text. Then appropriately set the connections. An element can be of any data type. The updating of SelectorObjects via elements are handled internally.
        '''

        # Set the elements
        if type(elements) == list:
            self.elements = elements
            self.page = 1
            self.maxPages = (len(self.elements) // self.elementsPerPage) + 1

        # Keep track of how much text has been added
        elementIndex = (self.page - 1) * self.elementsPerPage

        # Loop through each and every selectorTextObject
        for selectorText in self.getSelectorObjects():
            
            # As long as there are still elements to display, add the element text
            if elementIndex < len(self.elements):
                selectorText.updateSelectorObject(self.elements[elementIndex])
                selectorText.hasData = True
                elementIndex += 1
            
            # Otherwise, reset the text values
            else:
                selectorText.hasData = False
                selectorText.resetSelectorObject()

        # Lastly, update the connections
        self.setConnections()

    def getSelectorObjects(self) -> BaseSelectorObject:
        '''
        Generator for looping through each Selector object
        '''

        for j in range(self.gridDimensions[1]):
            for i in range(self.gridDimensions[0]):
                yield self.getSelectorObject((i, j))

    def getSelectorObject(self, position: Tuple[int, int]) -> BaseSelectorObject:
        '''
        Get the Selector Text object at a specific location in the selectorTextGrid. Passed in as an (x, y) pair
        '''

        return self.selectorGrid[position[1]][position[0]]

    def removeSelectorTextObject(self, position: Tuple[int, int]):
        self.getSelectorObject(self.selectedGridPositions.pop(self.selectedGridPositions.index(position))).isSelected = False

    def _onEvent(self, event: Event):
        '''
        When something happens to the selector object, make sure all the object's "isSelected" attribute gets correctly updated.
        '''

        # Look through each SelectorText object in the grid
        for selectorText in self.getSelectorObjects():

            # If the selector object is selected and it wasn't prevoius selected, toggle the selection and break out of the loop as only one object can be slected on each event.
            if selectorText.isSelected and selectorText.gridPosition not in self.selectedGridPositions:

                # If the maximum number of selected objects has already been reached, remove the first object selected from previousSelections
                if len(self.selectedGridPositions) == self.maxSelections:
                    self.getSelectorObject(self.selectedGridPositions.pop(0)).isSelected = False

                # Add the selector object to previous selections and break the loop
                self.selectedGridPositions.append(selectorText.gridPosition)
                break
                
            # If the selector object is not selected and it's in previous selections, remove it from previous selections
            if not selectorText.isSelected and selectorText.gridPosition in self.selectedGridPositions:
                self.selectedGridPositions.remove(selectorText.gridPosition)
        
        # Handle page flipping
        if self.paged:

            # TODO: Get the shift left, and right keys for windows
            if event.char == "F" and self.maxPages > self.page:
                self.page += 1
                self.updatePageText()
            elif event.char == "S" and self.page != 1:
                self.page -= 1
                self.updatePageText()

    def updatePageText(self):
        '''
        Whenever the page is changed, this updates the pageText object at the bottom of the screen which displays which page is currently being viewed.
        '''

        # First set the pageText
        self.pageText.text = "Page %i/%i" % (self.page, self.maxPages)

        # Then, make sure all previous selections are cleared.
        # TODO: Make selector compatible with selections on multiple pages
        while len(self.selectedGridPositions) > 0:
            self.getSelectorObject(self.selectedGridPositions.pop(0)).isSelected = False

        # Then set the text in each selectorObject to match the new page
        self.updateSelectorObjects()

    def _setValues(self):

        # Draw each selectorText object on the convas        
        for selectorObject in self.getSelectorObjects():
            selectorObject.drawOn(self)
        
        # If there are pages, draw that
        if self.paged:
            self.pageText.drawOn(self)
    
    def setConnections(self):
        '''
        Add the connections for each SelectionText object to the objectHandler
        '''
        
        # Clear whatever the current objectHandler connections are
        self.objectHandler.clearConnections()

        # Loop through each selectorText object to determine what connections need to be added
        for selectorObject in self.getSelectorObjects():

            # No need to do anything if the selectorObject contains no text
            if not selectorObject.hasData: continue

            # As long as the object isn't against the left or top of the grid, add the appropriate connections
            if selectorObject.gridPosition[0] > 0:
                self.objectHandler.addConnection(self.selectorGrid[selectorObject.gridPosition[1]][selectorObject.gridPosition[0] - 1], selectorObject, "R")
            if selectorObject.gridPosition[1] > 0:
                self.objectHandler.addConnection(self.selectorGrid[selectorObject.gridPosition[1] - 1][selectorObject.gridPosition[0]], selectorObject, "D")