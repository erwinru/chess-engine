# -*- coding: utf-8 -*-
import numpy as np


class AI:
    def __init__(self, board):
        self.b = board
        self.position_eval = []
        self.minmax_walkthroughs = 0
        pass

    def minimax(self, position, depth, maximizingPlayer):
        if depth == 0:
            return self.eval_board(position)
        if maximizingPlayer:
            maxEval = float("-inf")
            for child_position in self.b.get_child_positions(
                position, maximizingPlayer
            ):
                # from IPython import embed
                #
                # embed()
                eval = self.minimax(child_position, depth - 1, False)
                maxEval = max(maxEval, eval)
                self.minmax_walkthroughs += 1
            return maxEval
        else:
            minEval = float("inf")
            # from IPython import embed
            #
            # embed()
            for child_position in self.b.get_child_positions(
                position, maximizingPlayer
            ):
                # from IPython import embed
                #
                # embed()
                eval = self.minimax(child_position, depth - 1, True)
                minEval = min(minEval, eval)
                self.minmax_walkthroughs += 1
            return minEval

    def eval_board(self, position):
        return sum([piece.value for piece in self.b.get_pieces(position)])

    def move(self, best_eval, curr_player, curr_board):
        best_positions = [
            child
            for child in self.b.get_child_positions(curr_board, curr_player)
            if self.eval_board(child) == best_eval
        ]
        best_positions = np.array(best_positions)
        random = np.random.randint(0, best_positions.shape[0])
        selected_position = best_positions[random, :]
        self.b.board = selected_position
        moved_piece = self.b.update_piece_pos(selected_position)

        return selected_position, moved_piece
