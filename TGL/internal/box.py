from dataclasses import dataclass

@dataclass
class Box:
    '''
    Basic box class to stor a rectangle style object
    '''

    x: int
    y: int
    w: int
    h: int