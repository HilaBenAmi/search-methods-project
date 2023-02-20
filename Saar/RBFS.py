from sys import maxsize


# Given a problem instance, finding the solution using the RBFS Algorithm
class RBFSSolver:
    def __init__(self, board, heuristic='manhattan'):
        self.solution = []
        self.initial = board
        self.heuristic = heuristic
        self.nodes_expanded = 1
        self.history = {}

    def solve(self):
        node, _ = self.search(self.initial, maxsize)
        return node.f_value(self.heuristic) if node else None

    def search(self, node, f_limit):
        self.update_history(node)
        successors = []

        if getattr(node, self.heuristic) == 0:
            return node, None

        children = node.neighbours()

        count = -1
        for child in children:
            count += 1
            successors.append((child.rbfs_eval_f, count, child))

        if not len(successors):
            return None, maxsize

        while len(successors):
            successors.sort()
            best_node = successors[0][2]
            if best_node.rbfs_eval_f > f_limit:
                return None, best_node.rbfs_eval_f

            alternative = successors[1][0]
            result, best_node.rbfs_eval_f = self.search(best_node, min(f_limit, alternative))
            successors[0] = (best_node.rbfs_eval_f, successors[0][1], best_node)
            self.nodes_expanded += 1

            if result is not None:
                return result, None

    def reset_history(self):
        self.history = {}

    def update_history(self, board):
        board_str = str(board)
        if board_str not in self.history:
            self.history[board_str] = 1
        else:
            self.history[board_str] += 1
