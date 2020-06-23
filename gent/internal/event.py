# Copyright Clayton Brown 2019. See LICENSE file.

from dataclasses import dataclass

from asciimatics import event as asciimaticsEvent

from enum import Enum, auto

from typing import Tuple

class EVENT_HANDLER(Enum):

    HANDLED = auto()
    DID_NOT_HANDLE = auto()
    EXIT = auto()

class EVENTS(Enum):
    '''
    All normally supported utf-8 values can be accessed by event.keyNumber == ord(c) where c is the character to match.
    (These can also be accessed through the event.char value if you prefer, but only for events with a keyNumber that is
    greater than or equal to 0 and less than 256) Mouse events are automatically assigned an keyNumber of 1000.

    Special characters and mouse motions and clicks are listed here and can be accessed through event.key == EVENTS.[~~~]
    '''

    # Default for events which don't have special names
    NONE = auto()

    # Mouse events
    MOUSE_MOTION = auto()
    LEFT_CLICK = auto()
    RIGHT_CLICK = auto()
    DOUBLE_CLICK = auto()

@dataclass
class Event:
    '''
    Custom event types.
    '''

    # Event int value
    keyNumber: int = None

    # If this is a special event, that event is given an ID to match against EVENT.[~~~]
    ID: str = None

    # chr value of the key if it exists
    char: str = None

    # position of the mouse if it exists
    pos: Tuple[int] = None


# Map for createEvent() function to use to remember important characters
eventMap = {



}

# TERM=xterm-1003 to enable mouse movement events.
def createEvent(e: asciimaticsEvent) -> Event:
    '''
    Return a simple event object describing what input the user gave.
    '''

    if type(e) == asciimaticsEvent.KeyboardEvent:

        event = Event(
            e.key_code,
            eventMap[e.key_code] if e.key_code in eventMap else EVENTS.NONE,
            chr(e.key_code) if e.key_code >= 0 and e.key_code <= 255 else ""
        )

    if type(e) == asciimaticsEvent.MouseEvent:

        ID = EVENTS.MOUSE_MOTION
        if e.buttons == asciimaticsEvent.MouseEvent.LEFT_CLICK: ID = EVENTS.LEFT_CLICK
        elif e.buttons == asciimaticsEvent.MouseEvent.RIGHT_CLICK: ID = EVENTS.RIGHT_CLICK
        elif e.buttons == asciimaticsEvent.MouseEvent.DOUBLE_CLICK: ID = EVENTS.DOUBLE_CLICK
        
        event = Event(
            1000,
            ID,
            None,
            (e.x, e.y)
        )

    print(event)
    return event