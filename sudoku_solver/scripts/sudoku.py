import numpy as np


class Sudoku(object):

    def __init__(self, matrix=np.array([])):
        self.matrix = matrix
        self.squares = {}
        self.unknowns = []
        self.update()

    def update(self):
        """
        update unknowns cells and squares of sudoku
        :return:
        """
        self.get_unknowns()
        self.make_squares()

    def make_squares(self):
        """
        make a map of 9 square (by their coordinates)
        """

        for x in [0, 3, 6]:
            for y in [0, 3, 6]:
                matrix = self.matrix[x:x+3, y:y+3]
                square_zeros = [(x+i[0], y+i[1]) for i in np.argwhere(matrix == 0)]
                self.squares[((x, x+3), (y, y+3))] = {'matrix': matrix, 'zeros': square_zeros}

    def get_unknowns(self):
        """
        get indices of all 0 in matrix
        """
        self.unknowns = np.array(np.where(self.matrix == 0))
        return self.unknowns
