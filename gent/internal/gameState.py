# Copyright Clayton Brown 2019. See LICENSE file.

import pickle

from .timing import timeFunction

class GameState:
    '''
    This is the base gamestate class. Gamestate is used to monitor all aspects of the application.

    Any data which doesn't need to be attached to a game object (not visual), should be stored here.

    Each application should create a gamestate object which inherits from this.
    '''

    def __init__(self):
        self.__dict__ = {}

        # Current gameState time (in seconds)
        self.now: float = timeFunction()

        # The last gameState time (in seconds)
        self.last: float = timeFunction()


    ######################
    # SAVING AND LOADING #
    ######################
    def save(self, savePath: str):
        '''
        Saves the whole GameState into a pickle.
        '''

        with open(savePath, "wb") as f:
            pickle.dump(
                self.__dict__,
                f,
                protocol=pickle.HIGHEST_PROTOCOL
            )
    
    @staticmethod
    def load(loadPath: str) -> "GameState":
        '''
        Loads the whole GameState from a pickle.
        '''

        gameState = GameState()

        with open(loadPath, "rb") as f:
            gameState.__dict__ = pickle.load(f)

        return gameState
    

    ##########
    # TIMING #
    ##########
    def updateTime(self):
        '''
        Updates self.now and self.last. This function will be called before every game update.
        '''

        self.last = self.now
        self.now = timeFunction()
    
    def getFrameTime(self):
        '''
        Returns how long the last call of update was ago (in seconds)
        '''

        return self.now - self.last