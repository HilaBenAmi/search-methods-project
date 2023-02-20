from copy import copy

import numpy as np


class Board(object):
    """ A nxn board for with n^2 - 1 tiles
        ZERO COMES LAST
    """
    row_mul = 1
    edge_costs = {'u': 1,
                  'd': 1,
                  'l': 1 * row_mul,
                  'r': 1 * row_mul}

    def __init__(self, tiles=None, size=3):
        if tiles is None:
            self.dim = size
            self.tiles = self.generate_board(size)
            while not self.is_solvable():
                self.tiles = self.generate_board(size)
        else:
            self.dim = len(tiles)
            self.tiles = tiles

        self.zero_row = np.where(self.tiles == 0)[0][0]
        self.zero_column = np.where(self.tiles == 0)[1][0]
        self.manhattan = self._manhattan()
        self.hamming = self._hamming()
        self.g = 0
        self.rbfs_eval_f = self.manhattan

    def __copy__(self):
        cls = self.__class__
        new_copy = cls.__new__(cls)
        new_copy.tiles = np.copy(self.tiles)
        new_copy.manhattan = self.manhattan
        new_copy.hamming = self.hamming
        new_copy.dim = self.dim
        new_copy.zero_row = self.zero_row
        new_copy.zero_column = self.zero_column
        new_copy.g = self.g
        return new_copy

    def _manhattan(self):
        manhattan = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.tiles[i][j] != 0:
                    row = (self.tiles[i][j] - 1) // self.dim
                    column = (self.tiles[i][j] - 1) % self.dim
                    manhattan += (abs(i - row) * Board.row_mul) + abs(j - column)
        return manhattan

    def _hamming(self):  # aka tiles out of place
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                solution_row = (self.tiles[i][j] - 1) // self.dim
                solution_column = (self.tiles[i][j] - 1) % self.dim
                if self.tiles[i][j] != 0 and self.tiles[i][j] != self.tiles[solution_row][solution_column]:
                    res += 1
        return res

    def equals(self, board):
        """
        :param Board board: Test board
        """
        return np.array_equal(board.tiles, self.tiles)

    def swap_zero(self, i0, j0):
        """
        Swaps tile at i0, j0 with the zero tile. Updates the heuristics of the neighbor!
        """
        # Recalculate manhattan distance
        row = (self.tiles[i0][j0] - 1) // self.dim
        column = (self.tiles[i0][j0] - 1) % self.dim
        self.manhattan -= abs(i0 - row) + abs(j0 - column)
        self.manhattan += abs(self.zero_row - row) + abs(self.zero_column - column)

        # Recalculate hamming distance
        solution_row = (self.tiles[i0][j0] - 1) // self.dim
        solution_column = (self.tiles[i0][j0] - 1) % self.dim
        if solution_column == j0 and solution_row == i0:  # The change we made moved a non-zero tile FROM its goal place
            self.hamming += 1
        elif solution_column == self.zero_column and solution_row == self.zero_row:  # The change we made moved a non-zero tile TO its goal place
            self.hamming -= 1

        # Swap tiles
        self.tiles[i0][j0], self.tiles[self.zero_row, self.zero_column] = \
            self.tiles[self.zero_row, self.zero_column], self.tiles[i0, j0]
        # Update zero row and column
        self.zero_row = i0
        self.zero_column = j0

    def neighbours(self):
        neighbours = []

        # The zero tile can be swapped with tile above
        if self.zero_row > 0:
            neighbour = copy(self)
            neighbour.swap_zero(self.zero_row - 1, self.zero_column)
            neighbour.g = self.g + Board.edge_costs['d']
            neighbour.rbfs_eval_f = neighbour.g + neighbour.manhattan
            neighbours.append(neighbour)

        # The zero tile can be swapped with tile below
        if self.zero_row < self.dim - 1:
            neighbour = copy(self)
            neighbour.swap_zero(self.zero_row + 1, self.zero_column)
            neighbour.g = self.g + Board.edge_costs['u']
            neighbour.rbfs_eval_f = neighbour.g + neighbour.manhattan
            neighbours.append(neighbour)

        # The zero tile can be swapped with the tile to its left
        if self.zero_column > 0:
            neighbour = copy(self)
            neighbour.swap_zero(self.zero_row, self.zero_column - 1)
            neighbour.g = self.g + Board.edge_costs['r']
            neighbour.rbfs_eval_f = neighbour.g + neighbour.manhattan
            neighbours.append(neighbour)

        # The zero tile can be swapped with the tile to its right
        if self.zero_column < self.dim - 1:
            neighbour = copy(self)
            neighbour.swap_zero(self.zero_row, self.zero_column + 1)
            neighbour.g = self.g + Board.edge_costs['l']
            neighbour.rbfs_eval_f = neighbour.g + neighbour.manhattan
            neighbours.append(neighbour)

        return neighbours

    def f_value(self, heuristic='manhattan'):
        h = getattr(self, heuristic)
        return self.g + h

    def is_solved(self):
        """
        Checks if the board is the goal position
        """
        return self.manhattan == 0

    def is_solvable(self):
        """
        Checks if the board is solvable
        """
        tiles = np.ndarray.flatten(self.tiles)
        dim = self.dim * self.dim

        inversions = 0
        for i in range(dim):
            for j in range(i, dim):
                if tiles[i] != 0 and tiles[j] != 0 and tiles[i] > tiles[j]:
                    inversions += 1

        return inversions % 2 == 0

    @staticmethod
    def generate_board(size):
        arr = np.arange(size ** 2)
        np.random.shuffle(arr)
        arr = arr.reshape(size, size)
        return arr

    def __str__(self):
        return ''.join(str(d) for d in self.tiles.reshape(-1))

    def __lt__(self, nxt):
        return self.manhattan < nxt.manhattan
