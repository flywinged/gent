# Copyright Clayton Brown 2019. See LICENSE file.

# Examples control some example games (found in ./examples)
# Just do python3 examples.py <name> to run them

import sys

# Import all the examples
from examples.test import test

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        raise Exception("Please specify the game you want to play.")

    # Testing call
    if sys.argv[1] == "test":
        test()

    # Didn't call a valid game
    else:
        raise Exception(f"{sys.argv[1]} is not a recognized game. Try Again.")