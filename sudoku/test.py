"""
OOP method of solving sudoku
"""

from sudoku import *

# to solve a sudoku defined in data directory
solve("m18.data")

pass

# to solve a sudoku and just using the methods which level <= 15 and if can't solve, don't use guess method
solve("m3.data", level_limit=15, use_try=False)

pass

# to solve a sudoku with emulator methods and print the steps
solve("m12.data", use_emu=True, print_step=True)

pass

# to solve the world's best difficult sudoku
# by default method
solve("m10.data")

# by computer's try error
try_error(None, file="m10.data")

# by all methods but not using human guessing, it can't solve the sudoku
solve("m10.data", use_emu=True, use_try=False)

# by basic human methods and guess
solve("m10.data", level_limit=10, use_try=True)
solve("m10.data", level_limit=3, use_try=True)