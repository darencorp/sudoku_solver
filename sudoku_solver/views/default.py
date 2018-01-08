from numpy import matrix
from pyramid.view import view_config

from sudoku_solver.scripts import resolver
from sudoku_solver.scripts.resolver import recursive
from sudoku_solver.scripts.sudoku import Sudoku


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

    m = matrix(j)

    s = Sudoku(m)

    branches = dict()
    branches[1] = {'sudoku': s, 'unknowns': s.unknowns}

    result = resolver.recursive(s, s.unknowns, branches)

    if result:
        return result['sudoku'].matrix_list
    else:
        return False