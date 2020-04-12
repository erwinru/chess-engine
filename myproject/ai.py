# -*- coding: utf-8 -*-
import numpy as np


class AI:
    depth = 2

    def __init__(self, board, is_player_white):
        self.b = board
        self.is_ai_white = not is_player_white

        self.board_caches = {}
        pass

    def minimax(self, position, depth, is_maxing_white):
        if depth == 0:
            self.board_caches[
                self.hash_board(position, depth, is_maxing_white)
            ] = self.eval_board(position)
            return self.board_caches[self.hash_board(position, depth, is_maxing_white)]

        best_score = float("-inf") if is_maxing_white else float("inf")

        for child_pos in self.b.get_child_positions(position, is_maxing_white):
            local_score = self.minimax(child_pos, depth - 1, False)
            self.board_caches[
                self.hash_board(position, depth, is_maxing_white)
            ] = local_score

        if is_maxing_white:
            best_score = max(best_score, local_score)

        else:
            best_score = min(best_score, local_score)

        self.board_caches[
            self.hash_board(position, depth, is_maxing_white)
        ] = best_score

        return self.board_caches[self.hash_board(position, depth, is_maxing_white)]

    def hash_board(self, position, depth, is_maxing_white):
        return str(position) + " " + str(depth) + " " + str(is_maxing_white)

    def eval_board(self, position):
        return sum([piece.value for piece in self.b.get_pieces(position)])

    def move(self, position):
        global_score = float("-inf") if self.is_ai_white else float("inf")
        chosen_move = None

        for child_pos in self.b.get_child_positions(position, self.is_ai_white):

            local_score = self.minimax(child_pos, self.depth - 1, not self.is_ai_white)
            self.board_caches[
                self.hash_board(child_pos, self.depth - 1, not self.is_ai_white)
            ] = local_score

            if self.is_ai_white and local_score > global_score:
                global_score = local_score
                chosen_pos = child_pos
            elif not self.is_ai_white and local_score < global_score:
                global_score = local_score
                chosen_pos = child_pos

            print(local_score, child_pos)

        print(str(global_score) + " " + str(chosen_move) + "\n")

        self.b.board = chosen_pos
        moved_piece = self.b.update_piece_pos(chosen_pos)
        return chosen_pos, moved_piece
