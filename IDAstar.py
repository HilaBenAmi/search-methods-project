from sys import maxsize


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
            if t == maxsize:
                return 'NOT_FOUND'
            threshold = t

    def search(self, board, threshold):
        self.update_history(board)
        f = board.f_value(self.heuristic)
        if f > threshold:
            return f

        if getattr(board, self.heuristic) == 0:
            return 'FOUND'

        minimum = maxsize
        for next_board in board.get_possible_next_board():
            t = self.search(next_board, threshold)
            self.nodes_expanded += 1
            if t == 'FOUND':
                self.solution.append(board)
                return 'FOUND'
            if t < minimum:
                minimum = t
        return minimum

    def update_history(self, board):
        try:
            board_str = str(board)
            if board_str not in self.history:
                self.history[board_str] = 1
            else:
                self.history[board_str] += 1
        except:
            pass
