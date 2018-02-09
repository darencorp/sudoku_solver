from copy import deepcopy
from itertools import permutations
from sudoku_solver.scripts.sudoku import Sudoku

import numpy as np


class CellException(Exception):
    pass


branches = dict()

mx = np.array([[0, 7, 0, 0, 5, 0, 0, 9, 0],
               [2, 0, 0, 0, 0, 6, 4, 0, 0],
               [0, 9, 8, 0, 0, 2, 0, 0, 0],

               [0, 0, 9, 0, 0, 4, 0, 2, 0],
               [8, 0, 0, 0, 1, 0, 0, 0, 5],
               [0, 3, 0, 7, 0, 0, 8, 0, 0],

               [0, 0, 0, 6, 0, 0, 1, 8, 0],
               [0, 0, 1, 5, 0, 0, 0, 0, 7],
               [0, 8, 0, 0, 2, 0, 0, 6, 0]])


def resolve(matrix):
    sudoku = Sudoku(matrix)
    branches[1] = {'sudoku': sudoku}

    return recursive(sudoku)


def recursive(sudoku):
    """
    check sudoku for free cells, create new branch and fill free cells by test values
    :param sudoku: defined sudoku
    :return: exit from recursion is sudoku is resolved or found error in
    """

    if sudoku.unknowns[0].size != 0:  # check resolved sudoku

        check_single_cells(sudoku)  # fill all possible cells in current branch
        sudoku.update()  # update amount of unknowns for the next branch

        if sudoku.unknowns[0].size == 0:  # check resolved sudoku again
            return branches[len(branches)]  # end of recursion

        branches[len(branches) + 1] = deepcopy(branches[len(branches)])  # create new branch

        field = get_lowest_field(
            branches[len(branches)]['sudoku'])  # get field with the lowest amount of unknowns cells
        values = get_available_values(field, sudoku)  # get values needed to fill the field

        branch_values = permutations(values)  # get all possibles combinations of values

        error_field = None  # error in permutation for current branch

        for values in branch_values:

            # check if current permutation is not in error case
            if error_field is not None and values[error_field['index']] == error_field['value']:
                continue

            # fill branch with values of permutation
            branch_result = fill_branch(field, branches[len(branches)], list(values))

            # if error
            if not branch_result['result']:

                error_field = branch_result['error']  # save error case for current permutation

                branches.pop(len(branches))  # delete state of current branch
                branches[len(branches) + 1] = deepcopy(branches[len(branches)])  # make empty state for branch
            else:
                return branches[len(branches)]  # return filled field, end of recursion

        branches.pop(len(branches))  # if all permutations is faulted
        return False  # delete branch and go forward with previous branch

    else:
        return branches[len(branches)]  # end of recursion


def check_single_cells(sudoku):
    """
    check and fill single 0 in field for every unknown cell

    :param sudoku: next branch of sudoku
    :return: false if impossible to fill cell and true if ok
    """

    group_rows = np.bincount(sudoku.unknowns[0])  # get count of zeros in the each row
    filtered_rows = np.where(group_rows == 1)[0]  # get rows contained only 1 zero

    if filtered_rows.size != 0:  # if there are rows
        z_row = filtered_rows[0]  # get first row
        fill_single_cell(sudoku.matrix[z_row])  # fill zeros
        sudoku.update()  # update unknowns and squares
        check_single_cells(sudoku)  # check zeros again

    group_cols = np.bincount(sudoku.unknowns[1])  # get count of zeros in the each column
    filtered_cols = np.where(group_cols == 1)[0]  # get columns contained only 1 zero

    if filtered_cols.size != 0:
        z_col = filtered_cols[0]
        fill_single_cell(sudoku.matrix[..., z_col])  # fill zeros
        sudoku.update()
        check_single_cells(sudoku)

    filtered_square = list(x['matrix'] for x in sudoku.squares.values() if len(x['zeros']) == 1)

    if len(filtered_square) != 0:
        z_square = filtered_square[0]  # get squares with single zero
        fill_single_cell(z_square)
        sudoku.update()
        check_single_cells(sudoku)


def fill_single_cell(field):
    """
    fill the last cell in row or column or square

    :param field: row or column or square of sudoku
    """

    possibles = np.array(range(1, 10))  # all values in field
    mask = np.isin(possibles, field)  # mask necessary values in field
    target = possibles[np.argwhere(mask == False)[0][0]]  # get single lack of value
    field[field == 0] = target  # fill up the value


def get_lowest_field(sudoku):
    """
    get field with the lowest amount of unknowns in

    :return: index of field in sudoku, type of field
    """

    # get iterator over grouped rows by amount of unknowns
    row_iterator = np.nditer(np.bincount(sudoku.unknowns[0]), flags=['f_index'])

    # group rows by their position and amount of unknowns
    rows_map = np.array([[row_iterator.index, row] for row in row_iterator if row > 0])

    # order map by amount of unknowns, and get first
    lowest_row = np.sort(rows_map.view('i8,i8'), order=['f1'], axis=0).view(np.int)[0]

    # make dict with info of row_field
    row_filed = {'type': 'r', 'field': lowest_row[0], 'weight': lowest_row[1]}

    # do the same with columns
    col_iterator = np.nditer(np.bincount(sudoku.unknowns[1]), flags=['f_index'])

    # group columns by their position and amount of unknowns
    cols_map = np.array([[col_iterator.index, i] for i in col_iterator if i > 0])

    # order map by amount of unknowns, and get first
    lowest_col = np.sort(cols_map.view('i8,i8'), order=['f1'], axis=0).view(np.int)[0]

    # make dict with info of col_field
    col_field = {'type': 'c', 'field': lowest_col[0], 'weight': lowest_col[1]}

    # do the same with squares
    lowest_square = sorted(sudoku.squares.values(), key=lambda x: len(x['zeros']) if len(x['zeros']) > 0 else 10)[0]
    square_filed = {'type': 's', 'field': lowest_square['matrix'], 'weight': len(lowest_square['zeros']),
                    'zeros': lowest_square['zeros']}

    # get field with the lowest amount of unknowns
    return sorted([row_filed, col_field, square_filed], key=lambda x: x['weight'])[0]


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


def fill_branch(data_field, data, *args):
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

    for index, (x, v) in enumerate(zip(indices, values)):

        try:
            # fill the field of each type type
            if data_field['type'] == 'r':
                fill(data['sudoku'], (data_field['field'], x), v)  # for row

            elif data_field['type'] == 'c':
                fill(data['sudoku'], (x, data_field['field']), v)  # for column

            else:
                fill(data['sudoku'], (x[0], x[1]), v)  # for square

        except CellException as e:
            return {'result': False, 'error': {'index': index, 'value': v}}

    data['sudoku'].update()

    return {'result': recursive(data['sudoku']), 'error': None}


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
        raise CellException(value)

    if value in sudoku.matrix[..., axies[1]]:
        raise CellException(value)

    if value in square:
        raise CellException(value)

    sudoku.matrix[axies[0], axies[1]] = value  # fill up the value
