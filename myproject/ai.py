# -*- coding: utf-8 -*-


class AI:
    def __init__(self, position):
        self.position = position
        self.eval_board()
        pass

    def minimax(self, position, depth, maximizingPlayer):
        if depth == 0:
            return position.eval_board()
        if maximizingPlayer:
            maxEval = float("inf")
            for child in position.get_childpositions():
                eval = self.minimax(child, depth - 1, True)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float("inf")
            for child in position.get_child_positions():
                eval = self.minimax(child, depth - 1, False)
                minEval = min(minEval, eval)
            return minEval
