import numpy as np
from time import time

MAX_INT = np.iinfo(np.int64).max
MAX_ELAPSED_TIME = 60*10
MAX_EXPANDS_PER_ITER = 10


class IDAStarSolver:
    def __init__(self, board, heuristic='manhattan'):
        self.solution = []
        self.initial_board = board
        self.heuristic = heuristic
        self.nodes_expanded = 1
        self.history = {}
        self.s_time = time()

    def solve(self):
        threshold = getattr(self.initial_board, self.heuristic)

        while True:
            t = self.search(self.initial_board, threshold)
            if t == 'FOUND':
                return threshold
            if t == MAX_INT or time()-self.s_time > MAX_ELAPSED_TIME or t == 'NOT_FOUND':
                return 'NOT_FOUND'
            threshold = t

    def search(self, board, threshold):
        self.update_history(board)
        f = board.f_value(self.heuristic)
        if f > threshold:
            return f

        if getattr(board, self.heuristic) == 0:
            return 'FOUND'

        minimum = MAX_INT
        next_possible_board_list = board.get_possible_next_board(self.heuristic)
        for idx, next_board in enumerate(next_possible_board_list):
            t = self.search(next_board, threshold)
            self.nodes_expanded += 1
            if t == 'FOUND':
                self.solution.append(board)
                return 'FOUND'
            if t < minimum:
                minimum = t
            if idx == MAX_EXPANDS_PER_ITER and time()-self.s_time > MAX_ELAPSED_TIME:
                return 'NOT_FOUND'
        return minimum

    def update_history(self, board):
        board_str = str(board)
        if board_str not in self.history:
            self.history[board_str] = 1
        else:
            self.history[board_str] += 1
