from Sudoku.matrix import *

def test1(file):
    start = time.time()
    tryError(file=file)
    end = time.time()
    print("spend: {0}".format(end-start))
    start2 = time.time()
    TryError(file=file)
    end2 = time.time()
    print("spend: {0}".format(end2-start2))
