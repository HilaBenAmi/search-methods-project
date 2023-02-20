from sys import maxsize


# Given a problem instance, finding the solution using the IDA* Algorithm
class IDAStarSolver:
    def __init__(self, board, heuristic='manhattan'):
        self.solution = []
        self.initial = board
        self.heuristic = heuristic
        self.nodes_expanded = 1
        self.history = {}

    def solve(self):
        bound = getattr(self.initial, self.heuristic)

        while True:
            t = self.search(self.initial, bound)
            if t == 'FOUND':
                return bound
            if t == maxsize:
                return 'NOT_FOUND'
            bound = t

    def search(self, node, bound):
        self.update_history(node)
        f = node.f_value(self.heuristic)
        if f > bound:
            return f

        if getattr(node, self.heuristic) == 0:
            return 'FOUND'

        minimum = maxsize
        for neighbour in node.neighbours():
            t = self.search(neighbour, bound)
            self.nodes_expanded += 1
            if t == 'FOUND':
                self.solution.append(node)
                return 'FOUND'
            if t < minimum:
                minimum = t
        return minimum

    def moves(self):
        return len(self.solution)

    def reset_history(self):
        self.history = {}

    def update_history(self, board):
        board_str = str(board)
        if board_str not in self.history:
            self.history[board_str] = 1
        else:
            self.history[board_str] += 1
