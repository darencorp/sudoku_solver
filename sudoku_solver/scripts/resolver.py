from copy import deepcopy
from itertools import permutations
from numpy import matrix as m

mx = m([[0, 2, 0, 9, 0, 0, 8, 0, 0],
        [5, 9, 0, 4, 2, 0, 0, 3, 1],
        [3, 6, 0, 0, 0, 0, 0, 0, 4],

        [0, 0, 0, 7, 0, 6, 3, 9, 0],
        [0, 0, 0, 0, 5, 0, 7, 0, 0],
        [0, 8, 6, 0, 0, 9, 0, 0, 0],

        [6, 0, 0, 0, 0, 0, 0, 8, 9],
        [4, 7, 0, 0, 0, 8, 0, 0, 0],
        [0, 3, 1, 0, 0, 5, 0, 6, 0]])


def recursive(sudoku, unknowns, branches):
    if (len(unknowns) != 0):

        if check_single_cells(sudoku, unknowns):

            if len(unknowns) == 0:
                return branches[len(branches)]

            branches[len(branches) + 1] = deepcopy(branches[len(branches)])

            field = get_lowest_field(branches[len(branches)]['sudoku'])
            need_values = get_field_available(field, branches[len(branches)]['sudoku'])
            branch_values = permutations(need_values)

            for i in branch_values:
                if not make_branch(field, branches[len(branches)], branches, list(i)):
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


def check_single_cells(sudoku, unknowns):
    start_unknowns = len(unknowns)

    for cell in unknowns:
        if sudoku.squares[cell.square].get_unknowns_count() == 1:
            fill_cell(cell, sudoku.squares[cell.square].get_available()[0], sudoku)
            continue

        if get_unknowns_count(sudoku.matrix_list[cell.global_x]) == 1:
            fill_cell(cell, cell.get_row_available(sudoku)[0], sudoku)
            continue

        if get_unknowns_count(sudoku.matrix.getT().tolist()[cell.global_y]) == 1:
            fill_cell(cell, cell.get_column_available(sudoku)[0], sudoku)
            continue

    if start_unknowns > len(unknowns):
        r = check_single_cells(sudoku, unknowns)
        return r

    return True


def fill_cell(cell, value, sudoku):
    if value in sudoku.squares[cell.square].get_values():
        return False

    if value in sudoku.matrix_list[cell.global_x]:
        return False

    if value in sudoku.matrix.getT().tolist()[cell.global_y]:
        return False

    cell.value = value
    fill(sudoku, cell, value)
    return True


def fill(sudoku, cell, value):
    sudoku.matrix.itemset((cell.global_x, cell.global_y), value)
    sudoku.matrix_list[cell.global_x][cell.global_y] = value
    sudoku.squares[cell.square].elements[cell.local_x][cell.local_y] = value
    sudoku.unknowns.remove(cell)


def get_lowest_field(sudoku):
    squares = []
    rows = []
    columns = []

    for square in sudoku.squares.values():
        if square.get_unknowns_count() > 0:
            squares.append(
                {'index': square.get_unknowns_count(),
                 'cells': square.get_unknowns(),
                 'type': 's',
                 'key': square.position
                 }
            )

    for row in sudoku.matrix_list:
        if get_unknowns_count(row):
            rows.append(
                {'index': get_unknowns_count(row),
                 'cells': sudoku.get_unknowns_cells(row=sudoku.matrix_list.index(row)),
                 'type': 'r',
                 'key': sudoku.matrix_list.index(row)
                 }
            )

    for column in sudoku.matrix.getT().tolist():
        if get_unknowns_count(column):
            columns.append(
                {'index': get_unknowns_count(column),
                 'cells': sudoku.get_unknowns_cells(column=sudoku.matrix.getT().tolist().index(column)),
                 'type': 'c',
                 'key': sudoku.matrix.getT().tolist().index(column)
                 }
            )

    low_fields = [
        sorted(squares, key=lambda x: x['index'])[0],
        sorted(rows, key=lambda x: x['index'])[0],
        sorted(columns, key=lambda x: x['index'])[0]
    ]

    sorted_field = sorted(low_fields, key=lambda x: x['index'])

    return sorted_field[0]


def get_available(field):
    available_values = list(range(1, 10))

    for i in field:
        if i in available_values:
            available_values.remove(i)

    return available_values


def get_field_available(field, sudoku):
    if field['type'] == 's':
        return sudoku.squares[field['key']].get_available()

    elif field['type'] == 'r':
        return get_available(sudoku.matrix_list[field['cells'][0].global_x])

    else:
        return get_available(sudoku.matrix.getT().tolist()[field['cells'][0].global_y])


def get_unknowns_count(field):
    return len(get_available(field))


def make_branch(field, data, branches, *args):
    values = args[0]

    for i in values:
        if not fill_cell(field['cells'][values.index(i)], i, data['sudoku']):
            return False

    return recursive(data['sudoku'], data['unknowns'], branches)