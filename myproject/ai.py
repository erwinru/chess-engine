# -*- coding: utf-8 -*-
import numpy as np


class AI:
    depth = 3

    def __init__(self, board, is_player_white):
        self.b = board
        self.is_ai_white = not is_player_white
        self.board_caches = {}

    def minimax(self, depth, is_maxing_white, alpha, beta):
        # if board in cache
        if self.hash_board(depth, is_maxing_white) in self.board_caches:
            return self.board_caches[self.hash_board(depth, is_maxing_white)]

        # if depth is 0 or game is over

        if depth == 0:  # or len(self.b.get_all_legal_moves()) == 0
            self.board_caches[
                self.hash_board(depth, is_maxing_white)
            ] = self.eval_board()
            return self.board_caches[self.hash_board(depth, is_maxing_white)]

        best_score = float("-inf") if is_maxing_white else float("inf")
        for move in self.b.get_all_legal_moves():

            moved_piece = self.b.push(move)

            local_score = self.minimax(depth - 1, not is_maxing_white, alpha, beta)

            self.board_caches[
                self.hash_board(depth - 1, not is_maxing_white)
            ] = local_score

            if is_maxing_white:
                best_score = max(best_score, local_score)
                alpha = max(alpha, best_score)

            else:
                best_score = min(best_score, local_score)
                beta = min(beta, best_score)

            self.b.pop(moved_piece, move[0])

            if beta <= alpha:
                break

        self.board_caches[self.hash_board(depth, is_maxing_white)] = best_score
        return self.board_caches[self.hash_board(depth, is_maxing_white)]

    def hash_board(self, depth, is_maxing_white):
        return str(self.b.board[-1]) + " " + str(depth) + " " + str(is_maxing_white)

    def eval_board(self):
        return sum([piece.value for piece in self.b.get_pieces()])

    def move(self):
        global_score = float("-inf") if self.is_ai_white else float("inf")
        chosen_pos = None

        for move in self.b.get_all_legal_moves():

            moved_piece = self.b.push(move)

            local_score = self.minimax(self.depth - 1, not self.is_ai_white, -1e8, 1e8)
            self.board_caches[
                self.hash_board(self.depth - 1, not self.is_ai_white)
            ] = local_score

            if self.is_ai_white and local_score > global_score:
                global_score = local_score
                chosen_pos = move
            elif not self.is_ai_white and local_score < global_score:
                global_score = local_score
                chosen_move = move

            print(local_score, self.b.board[-1])
            self.b.pop(moved_piece, move[0])

        moved_piece = self.b.push(chosen_move)

        print(str(global_score) + " " + str(chosen_move) + "\n")

        moved_piece = self.b.update_piece_pos2(moved_piece, chosen_move[1])
        return moved_piece
