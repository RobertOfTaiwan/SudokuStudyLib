"""
Traditional method of solving sudoku
"""

from matrix import *

# solve it directly
m, n, p = main("m6.data")

# solve it by limit methods, it can't solve the sudoku
m, n, p = main("m3.data", methods=8)

# set the limit methods to the 10, and it can solve the sudoku
m, n, p = main("m3.data", methods=10)

# using the try error's method to solve the best difficult sudoku in the world
m, n, p = TryError("m10.data")

