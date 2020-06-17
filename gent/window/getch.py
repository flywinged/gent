from ..internal.event import createEvent

import platform

import time
from typing import List

from threading import Thread

from types import FunctionType

class GetchThread(Thread):
    '''
    The getch thread collect events continuously.
    '''

    def __init__(self):
        Thread.__init__(self)

        # Set thread running to false to stop the thread from running
        self.running: bool = True

        # List of ord values
        self.sequence: List[int] = []

        # Window implementation, just use the msvcrt library
        if platform.system() == "Windows":
            import msvcrt #pylint: disable=import-error
            def getchFunction():
                return ord(msvcrt.getwch())

        # Mac and linux implementations
        else:
            import tty, termios, sys #pylint: disable=import-error
            def getchFunction():
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ord(ch)
        
        # The getch function (Platform specific)
        self.getch: FunctionType = getchFunction

    def run(self):

        while self.running:

            # NOTE: I have no idea why these have to be separate, But I will keep them this way just to make sure everything works correctly
            getchReturn = self.getch()
            self.sequence.append(getchReturn)

class EventGetter:
    '''

    '''

    def __init__(self):

        self.getchThread: GetchThread = GetchThread()
        self.getchThread.start()
    
    def getEvent(self):
        while len(self.getchThread.sequence) == 0:
            time.sleep(10e-6)
        time.sleep(0.0001)
        
        eventTuple = tuple(self.getchThread.sequence)
        self.getchThread.sequence = []

        return createEvent(eventTuple)