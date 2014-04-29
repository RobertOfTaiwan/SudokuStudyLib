import time
import sudoku
import matrix


def test1(file):
    start = time.time()
    sudoku.try_error(file=file)
    end = time.time()
    print("spend: {0}".format(end-start))

    start2 = time.time()
    matrix.TryError(file=file)
    end2 = time.time()
    print("spend: {0}".format(end2-start2))
