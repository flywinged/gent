# Copyright Clayton Brown 2019. See LICENSE file.

import time as pythonTime

import sys

timeFunction = None

if sys.platform == "win32":
    timeFunction = pythonTime.clock
else:
    timeFunction = pythonTime.time
