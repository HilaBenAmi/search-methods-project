from copy import deepcopy
import numpy as np


class Board():
    def __init__(self, size=3, heuristic='manhattan'):
        self.dim = size
        self.tiles = self.generate_board(size)
        self.goal_board = self.generate_board(size, is_default_goal=True)
        while not self.is_solvable():
            self.tiles = self.generate_board(size)

        blank_cell = self._find_blank()
        self.zero_row = blank_cell[0][0]
        self.zero_column = blank_cell[1][0]

        self.g = 0
        self.manhattan = None
        self.hamming = None
        self.f = None

    def set_f(self, heuristic='manhattan'):
        if heuristic == 'manhattan':
            self.manhattan = self._manhattan()
        elif heuristic == 'hamming':
            self.hamming = self._hamming()
        self.f = getattr(self, heuristic)

    def _find_blank(self):
        return np.where(self.tiles == 0)

    def _manhattan(self):
        manhattan = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.tiles[i][j] != 0:
                    row, col = find_goal(self.tiles[i][j], self.goal_board)
                    manhattan += abs(i - row) + abs(j - col)
        return manhattan

    def _update_manhattan(self, prev_loc, next_loc):
        goal_row, goal_col = find_goal(self.tiles[prev_loc[0]][prev_loc[1]], self.goal_board)
        self.manhattan -= abs(prev_loc[0] - goal_row) + abs(prev_loc[1] - goal_col)
        self.manhattan += abs(next_loc[0] - goal_row) + abs(next_loc[1] - goal_col)

    def _hamming(self):
        res = 0
        for i in range(self.dim):
            for j in range(self.dim):
                row, col = find_goal(self.tiles[i][j], self.goal_board)
                if self.tiles[i][j] != 0 and self.tiles[i][j] != self.tiles[row][col]:
                    res += 1
        return res

    def _update_hamming(self, prev_loc, next_loc):
        goal_row, goal_col = find_goal(self.tiles[prev_loc[0]][prev_loc[1]], self.goal_board)
        if goal_row == prev_loc[0] and goal_col == prev_loc[1]:  # The change we made moved a non-zero tile FROM its goal place
            self.hamming += 1
        elif goal_row == next_loc[0] and goal_col == next_loc[1]:  # The change we made moved a non-zero tile TO its goal place
            self.hamming -= 1

    def swap_with_zero(self, next_zero_row, next_zero_col, heuristic='manhattan'):
        """
            Swaps tile at i0, j0 with the zero tile
            update manhattan and hamming
        """
        if heuristic == 'manhattan':
            self._update_manhattan(prev_loc=(next_zero_row, next_zero_col), next_loc=(self.zero_row, self.zero_column))
        elif heuristic == 'hamming':
            self._update_hamming(prev_loc=(next_zero_row, next_zero_col), next_loc=(self.zero_row, self.zero_column))

        # Swap tiles
        self.tiles[self.zero_row, self.zero_column] = self.tiles[next_zero_row, next_zero_col]
        self.tiles[next_zero_row][next_zero_col] = 0

        # Update zero row and column
        self.zero_row, self.zero_column = next_zero_row, next_zero_col

    def _create_next_board(self, next_row, next_col, heuristic='manhattan'):
        next_board = deepcopy(self)
        next_board.swap_with_zero(next_row, next_col, heuristic)
        next_board.g = self.g + 1
        next_board.eval_f = next_board.g + next_board.manhattan
        return next_board

    def get_possible_next_board(self, heuristic='manhattan'):
        next_board_list = []

        # The zero tile can be swapped with tile above
        if self.zero_row > 0:
            next_board = self._create_next_board(self.zero_row - 1, self.zero_column, heuristic)
            next_board_list.append(next_board)

        # The zero tile can be swapped with tile below
        if self.zero_row < self.dim - 1:
            next_board = self._create_next_board(self.zero_row + 1, self.zero_column, heuristic)
            next_board_list.append(next_board)

        # The zero tile can be swapped with the tile to its left
        if self.zero_column > 0:
            next_board = self._create_next_board(self.zero_row, self.zero_column - 1, heuristic)
            next_board_list.append(next_board)

        # The zero tile can be swapped with the tile to its right
        if self.zero_column < self.dim - 1:
            next_board = self._create_next_board(self.zero_row, self.zero_column + 1, heuristic)
            next_board_list.append(next_board)

        return next_board_list

    def f_value(self, heuristic='manhattan'):
        h = getattr(self, heuristic)
        return self.g + h

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

    def generate_board(self, size, is_default_goal=False):
        arr = np.arange(size * size)
        if not is_default_goal:
            np.random.shuffle(arr)
        arr = arr.reshape(size, size)
        return arr

    def __str__(self):
        return ''.join(str(d) for d in self.tiles.reshape(-1))

    def __lt__(self, nxt):
        return self.manhattan < nxt.manhattan


def find_goal(current_char, goal_board):
    """
        find the correct place of a tile the goal board
    """
    for i in range(len(goal_board)):
        for j in range(len(goal_board)):
            if goal_board[i][j] == current_char:
                return i, j
