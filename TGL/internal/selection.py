from .gameObject import Selection

from typing import Dict

import numpy

class Selection_Fill(Selection):
    '''

    '''

    # Default styles for the Selection_Fill
    SELECT_COLOR: tuple = (0, 255, 0)
    HOVER_COLOR: tuple = (200, 200, 0)
    DEFAULT_COLOR: tuple = (0, 0, 0)

    def __init__(self,
                 selectColor: tuple = None,
                 hoverColor: tuple = None,
                 defaultColor: tuple = None,
                 **kwargs):
        Selection.__init__(self, **kwargs)
        
        self.selectColor: tuple = selectColor
        self.hoverColor: tuple = hoverColor
        self.defaultColor: tuple = defaultColor

        if self.selectColor == None: self.selectColor = Selection_Fill.SELECT_COLOR
        if self.hoverColor == None: self.hoverColor = Selection_Fill.HOVER_COLOR
        if self.defaultColor == None: self.defaultColor = Selection_Fill.DEFAULT_COLOR
    
    def setBoxes(self):
        '''
        Overwrite the x, y, w, h, xOffset, and yOffset of the gameobject
        '''

        self.gameObject.x = self.gameObject.realX
        self.gameObject.y = self.gameObject.realY
        self.gameObject.w = self.gameObject.realW
        self.gameObject.h = self.gameObject.realH
        self.gameObject.xOffset = 0
        self.gameObject.yOffset = 0
    
    def _select(self):
        '''
        How to draw the selection indication about the gameObject
        '''

        self.gameObject.bufferCanvas.backgroundColors[:,:] = numpy.array(self.selectColor)
    
    def _hover(self):
        '''
        How to draw the hover indication about the gameObject
        '''

        self.gameObject.bufferCanvas.backgroundColors[:,:] = numpy.array(self.hoverColor)
    
    def _default(self):
        '''
        How to draw the default indication about the gameObject
        '''

        self.gameObject.bufferCanvas.backgroundColors[:,:] = numpy.array(self.defaultColor)

class Selection_Box(Selection):
    '''
    Selection Style which filles in parts of the object starting from the edges

    Parameters
    ----------
    select/hover/defaultStyle: The styles of the border when selected, hovered, or default

    borders: Dictionary describing the border in each direction
    '''

    # Default styles for the Selection_Box
    SELECT_COLOR: tuple = (0, 255, 0)
    HOVER_COLOR: tuple = (200, 200, 0)
    DEFAULT_COLOR: tuple = (0, 0, 0)

    def __init__(self, 
                 selectColor: tuple = None,
                 hoverColor: tuple = None,
                 defaultColor: tuple = None,
                 borders: Dict[str, int] = None,
                 **kwargs
                ):
        Selection.__init__(self, **kwargs)
        
        self.borders: Dict[str, int] = borders
        if borders == None:
            self.borders = {
                "t" : (1, 1),
                "l" : (1, 1),
                "b" : (1, 1),
                "r" : (1, 1)
            }

        self.selectColor: tuple = selectColor
        self.hoverColor: tuple = hoverColor
        self.defaultColor: tuple = defaultColor

        if self.selectColor == None: self.selectColor = Selection_Box.SELECT_COLOR
        if self.hoverColor == None: self.hoverColor = Selection_Box.HOVER_COLOR
        if self.defaultColor == None: self.defaultColor = Selection_Box.DEFAULT_COLOR
    
    def setBoxes(self):
        '''
        Overwrite the x, y, w, h, xOffset, and yOffset of the gameobject
        '''

        if "t" in self.borders:
            self.gameObject.yOffset = self.borders["t"][1]
            self.gameObject.y = self.gameObject.realY + self.gameObject.yOffset
        else:
            self.gameObject.y = self.gameObject.realY

        if "l" in self.borders:
            self.gameObject.xOffset = self.borders["l"][1]
            self.gameObject.x = self.gameObject.realX + self.gameObject.xOffset
        else:
            self.gameObject.x = self.gameObject.realX
        
        if "b" in self.borders:
            self.gameObject.h = self.gameObject.realH - self.gameObject.yOffset - self.borders["b"][1]
        else:
            self.gameObject.h = self.gameObject.realH - self.gameObject.yOffset
        
        if "r" in self.borders:
            self.gameObject.w = self.gameObject.realW - self.gameObject.xOffset - self.borders["r"][1]
        else:
            self.gameObject.w = self.gameObject.realW - self.gameObject.xOffset
    
    def draw(self, color: tuple):
        if "t" in self.borders:
            self.gameObject.bufferCanvas.backgroundColors[:,:self.borders["t"][0]] = numpy.array(color)

        if "l" in self.borders:
            self.gameObject.bufferCanvas.backgroundColors[:self.borders["l"][0],:] = numpy.array(color)

        if "b" in self.borders:
            self.gameObject.bufferCanvas.backgroundColors[:,self.gameObject.realH - self.borders["b"][0]] = numpy.array(color)

        if "r" in self.borders:
            self.gameObject.bufferCanvas.backgroundColors[self.gameObject.realW - self.borders["r"][0],:] = numpy.array(color)

    def _select(self):
        '''
        How to draw the selection indication about the gameObject
        '''

        self.draw(self.selectColor)

    def _hover(self):
        '''
        How to draw the hover indication about the gameObject
        '''

        self.draw(self.hoverColor)
    
    def _default(self):
        '''
        How to draw the default indication about the gameObject
        '''

        self.draw(self.defaultColor)