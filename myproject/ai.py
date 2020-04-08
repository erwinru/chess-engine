# -*- coding: utf-8 -*-
import numpy as np


class AI:
    def __init__(self, board):
        self.b = board
        pass

    def minimax(self, position, depth, maximizingPlayer):
        if depth == 0:
            return self.eval_board(position)
        if maximizingPlayer:
            maxEval = float("-inf")
            for child_position in self.b.get_child_positions(
                position, maximizingPlayer
            ):
                eval = self.minimax(child_position, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float("inf")
            for child_position in self.b.get_child_positions(
                position, maximizingPlayer
            ):
                self.b.get_child_positions
                eval = self.minimax(child_position, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

    def eval_board(self, position):
        return sum([piece.value for piece in self.b.get_pieces(position)])

    def move(self, best_eval, curr_player, curr_board):
        best_positions = [
            child
            for child in self.b.get_child_positions(self.b.board, curr_player)
            if self.eval_board(child) == best_eval
        ]
        best_positions = np.array(best_positions)
        random = np.random.randint(0, best_positions.shape[0])
        selected_position = best_positions[random, :]
        self.b.board = selected_position
        for piece in self.b.get_pieces(selected_position):
            if piece.pos != self.b.find_board_coordinates(piece):
                moved_piece = piece
                piece.pos = self.b.find_board_coordinates(piece)

        return selected_position, moved_piece
