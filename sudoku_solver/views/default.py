from pyramid.view import view_config
from sudoku_solver.scripts import resolver as stochastic
from sudoku_solver.scripts import constraint_resolver as constraint

import numpy as np


@view_config(route_name='home', renderer='../templates/index.html')
def my_view(request):
    return dict()


@view_config(route_name='sudoku', renderer='json')
def sudoku(request):
    return stochastic.mx.tolist()


@view_config(route_name='resolve', renderer='json')
def resolve(request):
    r = request

    j = r.json

    sudoku = j.get('sudoku', None)

    if sudoku is None:
        return False

    sudoku_array = np.array(sudoku)

    sudoku_array[sudoku_array == None] = 0
    sudoku_array[sudoku_array == ''] = 0
    sudoku_array.astype(int)

    if j['type'] == 'constraint':
        result = constraint.resolve(sudoku_array)
    else:
        result = stochastic.resolve(sudoku_array)

    if result is not None:
        return np.asanyarray(result, dtype=np.int16).tolist()
    else:
        return False
