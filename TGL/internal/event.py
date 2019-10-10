from dataclasses import dataclass

from enum import Enum, auto

from typing import Tuple

from sys import platform

class EVENT_HANDLER(Enum):

    HANDLED = auto()
    DID_NOT_HANDLE = auto()
    EXIT = auto()

EVENT_MAP = {

    (3, ) : "EXIT",

    (8, ):  "BACKSPACE",
    (9, ):  "TAB",
    (13, ): "RETURN",
    (27, ): "ESCAPE",

    (32, ): "SPACE",

    (127, ): "BACKSPACE"
   
}

WINDOWS_EVENT_MAP = {

    (224, 72): "UP",
    (224, 75): "LEFT",
    (224, 77): "RIGHT",
    (224, 80): "DOWN",

    (0, 59): "F1",
    (0, 60): "F2",
    (0, 61): "F3",
    (0, 62): "F4",
    (0, 63): "F5",
    (0, 64): "F6",
    (0, 65): "F7",
    (0, 66): "F8",
    (0, 67): "F9",
    (0, 68): "F10",
    (224, 133): "F11",
    (224, 134): "F12",

    (224, 71): "HOME",
    (224, 73): "PAGE_UP",
    (224, 79): "END",
    (224, 81): "PAGE_DOWN",
    (224, 82): "INSERT",
    (224, 83): "DELETE",

}

LINUX_EVENT_MAP = {

    (27, 91, 65): "UP",
    (27, 91, 68): "LEFT",
    (27, 91, 67): "RIGHT",
    (27, 91, 66): "DOWN",

    (27, 91, 49, 59, 50, 65): "SHIFT_UP",
    (27, 91, 49, 59, 50, 68): "SHIFT_LEFT",
    (27, 91, 49, 59, 50, 67): "SHIFT_RIGHT",
    (27, 91, 49, 59, 50, 66): "SHIFT_DOWN",

    (27, 79, 80): "F1",
    (27, 79, 81): "F2",
    (27, 79, 82): "F3",
    (27, 79, 83): "F4",
    (27, 91, 49, 53, 126): "F5",
    (27, 91, 49, 55, 126): "F6",
    (27, 91, 49, 56, 126): "F7",
    (27, 91, 49, 57, 126): "F8",
    (27, 91, 50, 48, 126): "F9",

    (27, 91, 72): "HOME",
    (27, 91, 53, 126): "PAGE_UP",
    (27, 91, 70): "END",
    (27, 91, 54, 126): "PAGE_DOWN",
    (27, 91, 50, 126): "INSERT",
    (27, 91, 50, 126): "DELETE",

}

@dataclass
class Event:
    '''
    Custom event types.
    '''

    # Return value of getch
    keyNumber: Tuple[int] = None

    # name of the key
    keyName: str = None

    # Character Value
    char: str = None

def createEvent(e):
    '''

    '''

    event = Event()
    if len(e) == 1:
        event.char = chr(e[0])
        event.keyName  = chr(e[0])

    if e in EVENT_MAP:
        event.keyName = EVENT_MAP[e]
    
    elif "win" in platform.lower() and e in WINDOWS_EVENT_MAP:
        event.keyName = WINDOWS_EVENT_MAP[e]
    
    elif e in LINUX_EVENT_MAP:
        event.keyName = LINUX_EVENT_MAP[e]

    event.keyNumber = e

    return event
