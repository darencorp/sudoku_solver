import numpy as np

from constraint import *


def resolve(sudoku_array=np.zeros(shape=(9, 9), dtype=np.int16)):

    # create iterator through each element of array
    sudoku_iterator = np.nditer(sudoku_array, flags=['multi_index', 'refs_ok'])

    # map sudoku in array [((x,y): value), ...]
    sudoku_map = [(sudoku_iterator.multi_index, i.tolist()) for i in sudoku_iterator]

    # problem for constrains
    problem = Problem(RecursiveBacktrackingSolver())

    # make variables
    # iterate through x-axis of array
    for i in sudoku_map:

        # if element is unknown
        if i[1] == 0:
            # put in problem all possibles values from 0 to 9 on given index
            problem.addVariable(i[0], range(1, 10))
        else:
            # else put given value
            problem.addVariable(i[0], [i[1]])

    # make constrains for x,y axes

    # iterate through one of axis
    for axis, v in enumerate(sudoku_array.tolist()):

        # make constraint for each element of give axis (all different numbers in col/row)
        problem.addConstraint(AllDifferentConstraint(), [(axis, j) for j in range(9)])
        problem.addConstraint(AllDifferentConstraint(), [(j, axis) for j in range(9)])

    # make constraint for squares

    # loops for edge axes for squares
    for x in [0, 3, 6]:
        for y in [0, 3, 6]:

            # get next square indices
            square = np.argwhere(sudoku_array == sudoku_array).reshape(9, 9, 2)[x:x + 3, y:y + 3, ...].reshape(9, 2).tolist()

            # convert them to tuple
            square = list(map(lambda i: tuple(i), square))

            # make constraint for given square (all different numbers in square)
            problem.addConstraint(AllDifferentConstraint(), square)

    solution = problem.getSolution()

    if solution is None:
        return None

    result = np.empty(shape=(9, 9), dtype=np.int16)
    [result.itemset((k[0], k[1]), v) for k, v in solution.items()]

    return result