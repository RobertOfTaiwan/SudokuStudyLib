import os

from .sudoku import *

"""Init the status' values"""
# the index of the methods loops
Status.name["methodLoopIdx"] = 0

# the method idx which run now
Status.name["methodIdx"] = 0

# set this variable, if you want to make an exception when this position has been set
Status.name["checkPos"] = None

# if the every un-assigned positions have been writen down their possible number?
Status.name["writeDownAlready"] = False

# to set the possibles when using emulate method, for both positions and numbers
Status.name["emulatePossibles"] = 2

# the following using in guess()
Status.name["tryStack"] = []
Status.name["tryIdx"] = 0
Status.name["tryUse"] = True

# if use emulator method or not
Status.name["emuUse"] = True

# the scope of difficult level
Status.name["Scope"] = 0

# the level Limit, 0 means no limit
Status.name["Level"] = 0

# the Original Matrix
Status.name["Original"] = None

# the Result Matrix
Status.name["Result"] = None

# if print the steps of solving
Status.name["printStep"] = False

# record now path
Status.name["nowPath"] = os.path.abspath(os.path.dirname(sudoku.__file__))
os.chdir(Status.name["nowPath"])


