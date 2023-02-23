import heapq


class AStarSolver:
    def __init__(self, board, heuristic='manhattan'):
        self.solution = []
        self.initial_board = board
        self.heuristic = heuristic
        self.nodes_expanded = 1
        self.history = {}

    def solve(self):
        frontier = []
        heapq.heappush(frontier, (self.initial_board.f_value(self.heuristic), self.initial_board))

        while frontier:
            f, board = heapq.heappop(frontier)
            if getattr(board, self.heuristic) == 0:
                self.solution.append(board)
                return f

            if str(board) not in self.history:
                self.history[str(board)] = f
                next_possible_board_list = board.get_possible_next_board(self.heuristic)
                for next_board in next_possible_board_list:
                    heapq.heappush(frontier, (next_board.f_value(self.heuristic), next_board))
                    self.nodes_expanded += 1

        return 'NOT_FOUND'
