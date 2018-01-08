from numpy import matrix as m


class Sudoku(object):
    def __init__(self, matrix=m([])):
        self.matrix = matrix
        self.matrix_list = self.matrix.tolist()
        self.squares = dict()
        self.unknowns = []
        self.make_squares()
        self.get_all_unknowns()

    def make_squares(self):
        sudoku_matrix = [self.matrix_list[0:3], self.matrix_list[3:6], self.matrix_list[6:10]]

        square_position = 1

        for layer in sudoku_matrix:
            column_index = 0
            for i in range(0, 3):
                elements = []
                cells = []
                for row in layer:
                    for subrow in [(row[column_index:column_index + 3])]:
                        for cell in subrow:
                            global_x = sudoku_matrix.index(layer) * 3 + layer.index(row)
                            global_y = row.index(cell)
                            local_x = layer.index(row)
                            local_y = subrow.index(cell)
                            row[row.index(cell)] = -1 if cell == None else cell
                            self.matrix.itemset((global_x, global_y), -1) if cell == None else self.matrix.itemset(
                                (global_x, global_y), cell)
                            self.matrix_list[global_x][global_y] = -1 if cell == None else cell
                            cell = -1 if cell == 0 else cell
                            cells.append(
                                Cell(cell, square_position, (cell is None or cell <= 0), global_x, global_y, local_x, local_y))

                        elements.append(subrow)

                column_index += 3
                self.squares[square_position] = Square(square_position, elements, cells)
                square_position += 1

    def get_all_unknowns(self):
        for square in self.squares.values():
            for cell in square.cells:
                if cell.is_null:
                    self.unknowns.append(cell)

        return self.unknowns

    def is_valid(self):
        for i in self.matrix_list:
            if -1 in i or len(set(i)) != 9:
                return False

        for i in self.matrix.getT().tolist():
            if -1 in i or len(set(i)) != 9:
                return False

        validation = True

        # filter(lambda x: x if len(set(x)) == 9 else None, self.squares)

        return validation

    def get_unknowns_cells(self, row=None, column=None):
        if row != None:
            return list(filter(lambda x: x.global_x == row, self.unknowns))

        else:
            return list(filter(lambda x: x.global_y == column, self.unknowns))


class Square(object):
    def __init__(self, position=0, elements=[], cells=[]):
        self.position = position
        self.elements = elements
        self.cells = cells

    def get_unknowns(self):
        return list(filter(lambda x: x.value == 0 or x.value == -1 or x.value is None, self.cells))

    def get_unknowns_count(self):
        return len(self.get_unknowns())

    def get_values(self):
        values = []

        for cell in self.cells:
            if not cell.is_null:
                values.append(cell.value)

        return values

    def get_available(self):
        available_values = list(range(1, 10))

        for cell in self.cells:
            if cell.value in available_values:
                available_values.remove(cell.value)

        return available_values


class Cell(object):
    def __init__(self, val=0, square=0, is_null=True, global_x=0, global_y=0, local_x=0, local_y=0):
        self.value = val
        self.square = square
        self.is_null = is_null
        self.global_x = global_x
        self.global_y = global_y
        self.local_x = local_x
        self.local_y = local_y

    def get_row_available(self, sudoku):
        available_values = list(range(1, 10))

        for i in sudoku.matrix_list[self.global_x]:
            if i in available_values:
                available_values.remove(i)

        return available_values

    def get_column_available(self, sudoku):
        available_values = list(range(1, 10))

        for i in sudoku.matrix.getT().tolist()[self.global_y]:
            if i in available_values:
                available_values.remove(i)

        return available_values