from copy import deepcopy
from itertools import permutations

from sudoku_solver.scripts.sudoku import Sudoku
import numpy as np


class MyException(Exception):
    pass


mx = np.array([[0, 7, 0, 0, 5, 0, 0, 9, 0],
               [2, 0, 0, 0, 0, 6, 4, 0, 0],
               [0, 9, 8, 0, 0, 2, 0, 0, 0],

               [0, 0, 9, 0, 0, 4, 0, 2, 0],
               [8, 0, 0, 0, 1, 0, 0, 0, 5],
               [0, 3, 0, 7, 0, 0, 8, 0, 0],

               [0, 0, 0, 6, 0, 0, 1, 8, 0],
               [0, 0, 1, 5, 0, 0, 0, 0, 7],
               [0, 8, 0, 0, 2, 0, 0, 6, 0]])

branches = dict()


def resolve(matrix):
    matrix[matrix == None] = 0
    sudoku = Sudoku(matrix)
    branches[1] = {'sudoku': sudoku}

    return recursive(sudoku)


def recursive(sudoku):
    """
    check sudoku for free cells, create new branch and fill free cells by test values
    :param sudoku: defined sudoku
    :return: exit from recursion is sudoku is resolved or found error in
    """

    if sudoku.unknowns[0].size != 0:

        if check_single_cells(sudoku):

            sudoku.update()

            if sudoku.unknowns[0].size == 0:
                return branches[len(branches)]

            branches[len(branches) + 1] = deepcopy(branches[len(branches)])  # create new branch

            field = get_lowest_field(branches[len(branches)]['sudoku'])
            values = get_available_values(field, sudoku)

            branch_values = permutations(values)

            for i in branch_values:
                if not make_branch(field, branches[len(branches)], list(i)):
                    branches.pop(len(branches))
                    branches[len(branches) + 1] = deepcopy(branches[len(branches)])
                    field = get_lowest_field(branches[len(branches)]['sudoku'])
                else:
                    return branches[len(branches)]

            branches.pop(len(branches))
            return False

        else:
            return False
    else:
        return branches[len(branches)]


def check_single_cells(sudoku):
    """
    check and fill single 0 in field for every unknown cell

    :param sudoku: next branch of sudoku
    :return: false if impossible to fill cell and true if ok
    """
    try:
        group_rows = np.bincount(sudoku.unknowns[0])  # get count of zeros in the each row
        filtered_rows = np.where(group_rows == 1)[0]  # get rows contained only 1 zero

        if filtered_rows.size != 0:  # if there are rows
            z_row = filtered_rows[0]  # get first row
            fill_single_cell(sudoku, sudoku.matrix[z_row], row=z_row)  # fill zeros
            sudoku.update()  # update unknowns and squares
            check_single_cells(sudoku)  # check zeros again

        group_cols = np.bincount(sudoku.unknowns[1])  # get count of zeros in the each column
        filtered_cols = np.where(group_cols == 1)[0]  # get columns contained only 1 zero

        if filtered_cols.size != 0:
            z_col = filtered_cols[0]
            fill_single_cell(sudoku, sudoku.matrix[..., z_col], col=z_col)  # fill zeros
            sudoku.update()
            check_single_cells(sudoku)

        filtered_square = list(
            {'matrix': y['matrix'], 'x': y['zeros'][0][0], 'y': y['zeros'][0][1]} for x, y in sudoku.squares.items()
            if len(y['zeros']) == 1)

        if len(filtered_square) != 0:
            z_square = filtered_square[0]  # get squares with single zero
            fill_single_cell(sudoku, z_square['matrix'], row=z_square['x'], col=z_square['y'])
            sudoku.update()
            check_single_cells(sudoku)

    except MyException:
        return False

    return True


def fill_single_cell(sudoku, field, row=None, col=None):
    """
    fill the last cell in row or column or square

    :param field: row or column or square of sudoku
    :param row: index of row in sudoku
    :param col: index of col in sudoku
    """

    square = field if row is not None and col is not None else None  # get square from field if field is square

    row = np.where(field == 0)[0][0] if row is None else row  # get row if row is not set
    col = np.where(field == 0)[0][0] if col is None else col  # get column if column is not set

    square = sudoku.squares[
        filter(lambda x: sudoku.squares[x] if x[0][0] <= row < x[0][1] and x[1][0] <= col < x[1][1] else None,
               sudoku.squares.keys()).__next__()][
        'matrix'] if square is None else square  # get square form sudoku if field is not square

    possibles = np.array(range(1, 10))
    mask = np.isin(possibles, field)  # mask necessary values in field
    target = possibles[np.argwhere(mask == False)[0][0]]  # get single lack of value

    if target not in sudoku.matrix[row] and target not in sudoku.matrix[
        ..., col] and target not in square:  # check for error
        sudoku.matrix[row][col] = target  # fill field
    else:
        raise MyException

    return True


def get_lowest_field(sudoku):
    """
    get field with the lowest amount of unknowns in

    :return: index of field in sudoku, type of field
    """

    row_iterator = np.nditer(np.bincount(sudoku.unknowns[0]),
                             flags=['f_index'])  # get iterator over grouped rows by amount of unknowns
    rows_map = np.array([[row_iterator.index, i] for i in row_iterator if
                         i > 0])  # group rows by their position and amount of unknowsn
    lowest_row = np.sort(rows_map.view('i8,i8'), order=['f1'], axis=0).view(np.int)[
        0]  # order map by amount of unknowns, and get first
    row_filed = {'type': 'r', 'field': lowest_row[0], 'weight': lowest_row[1]}  # make dict with info of row_field

    col_iterator = np.nditer(np.bincount(sudoku.unknowns[1]), flags=['f_index'])  # make the same with columns
    cols_map = np.array([[col_iterator.index, i] for i in col_iterator if i > 0])
    lowest_col = np.sort(cols_map.view('i8,i8'), order=['f1'], axis=0).view(np.int)[0]
    col_field = {'type': 'c', 'field': lowest_col[0], 'weight': lowest_col[1]}

    lowest_square = sorted(sudoku.squares.values(), key=lambda x: len(x['zeros']) if len(x['zeros']) > 0 else 10)[
        0]  # and squares
    square_filed = {'type': 's', 'field': lowest_square['matrix'], 'weight': len(lowest_square['zeros']),
                    'zeros': lowest_square['zeros']}

    return sorted([row_filed, col_field, square_filed], key=lambda x: x['weight'])[
        0]  # get field with the lowest amount of unknowns


def get_available_values(field_index, sudoku):
    """
    get values witch may be filled inside of field

    :param field_index: index of field and type of field in sudoku
    :return: possibles values of field
    """

    if field_index['type'] == 'r':
        field = sudoku.matrix[field_index['field']]  # get row if field is row

    elif field_index['type'] == 'c':
        field = sudoku.matrix[..., field_index['field']]  # get column if column

    else:
        field = field_index['field']  # otherwise get square

    possibles = np.array(range(1, 10))
    mask = np.isin(possibles, field)

    return possibles[np.argwhere(mask == False)].flatten()


def make_branch(data_field, data, *args):
    """
    make new branch of sudoku and fill field through multiple values
    :param data_field: filed for filling
    :param data: new branch for sudoku
    :param args: values for filling
    :return: recursive sudoku filling or False if something is going wrong
    """
    values = args[0]

    if data_field['type'] == 'r':
        field = data['sudoku'].matrix[data_field['field']]  # get row if field is row
        indices = np.argwhere(field == 0).flatten()  # get indices of unknowns in row

    elif data_field['type'] == 'c':
        field = data['sudoku'].matrix[..., data_field['field']]  # get column if column
        indices = np.argwhere(field == 0).flatten()  # get indices of unknowns in column
    else:
        indices = data_field['zeros']  # get indices of unknowns in square

    for i, j in zip(indices, values):

        try:
            # fill field depends on it type
            if data_field['type'] == 'r':
                fill(data['sudoku'], (data_field['field'], i), j)  # for row

            elif data_field['type'] == 'c':
                fill(data['sudoku'], (i, data_field['field']), j)  # for column

            else:
                fill(data['sudoku'], (i[0], i[1]), j)  # for square

        except MyException:
            return False

    data['sudoku'].update()

    return recursive(data['sudoku'])


def fill(sudoku, axies, value):
    """
    fill sudoku cell up with the value

    :param sudoku: sudoku
    :param axies: indices of cell
    :param value: value
    """
    square = sudoku.squares[
        filter(lambda x: sudoku.squares[x] if x[0][0] <= axies[0] < x[0][1] and x[1][0] <= axies[1] < x[1][
            1] else None,
               sudoku.squares.keys()).__next__()]['matrix']  # get square for axis values

    # check cell for error
    if value in sudoku.matrix[axies[0]]:
        raise MyException

    if value in sudoku.matrix[..., axies[1]]:
        raise MyException

    if value in square:
        raise MyException

    sudoku.matrix[axies[0], axies[1]] = value
