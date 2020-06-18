# Copyright Clayton Brown 2019. See LICENSE file.

from dataclasses import dataclass

@dataclass
class Box:
    '''
    Basic box class to store a rectangle style object.
    These are the base for basically everything in gent.
    '''

    x: int
    y: int
    w: int
    h: int