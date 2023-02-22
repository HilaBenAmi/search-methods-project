import numpy as np

max_int = np.iinfo(np.int64).max


class IDAStarSolver:
    def __init__(self, board, heuristic='manhattan'):
        self.solution = []
        self.initial_board = board
        self.heuristic = heuristic
        self.nodes_expanded = 1
        self.history = {}

    def solve(self):
        threshold = getattr(self.initial_board, self.heuristic)

        while True:
            t = self.search(self.initial_board, threshold)
            if t == 'FOUND':
                return threshold
            if t == max_int:
                return 'NOT_FOUND'
            threshold = t

    def search(self, board, threshold):
        self.update_history(board)
        f = board.f_value(self.heuristic)
        if f > threshold:
            return f

        if getattr(board, self.heuristic) == 0:
            return 'FOUND'

        minimum = max_int
        next_possible_board_list = board.get_possible_next_board(self.heuristic)
        for next_board in next_possible_board_list:
            t = self.search(next_board, threshold)
            self.nodes_expanded += 1
            if t == 'FOUND':
                self.solution.append(board)
                return 'FOUND'
            if t < minimum:
                minimum = t
        return minimum

    def update_history(self, board):
        board_str = str(board)
        if board_str not in self.history:
            self.history[board_str] = 1
        else:
            self.history[board_str] += 1
