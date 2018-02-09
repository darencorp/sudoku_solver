from pyramid.view import view_config
from sudoku_solver.scripts import resolver

import numpy as np


@view_config(route_name='home', renderer='../templates/index.html')
def my_view(request):
    return dict()


@view_config(route_name='sudoku', renderer='json')
def sudoku(request):
    return resolver.mx.tolist()


@view_config(route_name='resolve', renderer='json')
def resolve(request):
    r = request

    j = r.json
    matrix = np.array(j)
    matrix[matrix == None] = 0
    result = resolver.resolve(matrix)

    if result:
        return np.asanyarray(result['sudoku'].matrix, dtype=np.int16).tolist()
    else:
        return False
