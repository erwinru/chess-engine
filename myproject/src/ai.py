# -*- coding: utf-8 -*-
import os

import numpy as np
import pickle


class AI:
    depth = 3

    notation_dict_x = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    notation_dict_y = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

    board_caches = {}

    if not os.path.exists("../data/"):
        os.mkdir("../data/")

    try:
        cache = open("../data/cache.p", "rb")
    except IOError:
        cache = open("data/cache.p", "wb")
        pickle.dump(board_caches, cache)
    else:
        board_caches = pickle.load(cache)

    def __init__(self, board, is_player_white):
        self.b = board
        self.is_ai_white = not is_player_white

    def minimax(self, depth, is_maxing_white, alpha, beta):
        # if board in cache
        if self.hash_board(depth, is_maxing_white) in self.board_caches:
            return self.board_caches[self.hash_board(depth, is_maxing_white)]

        # if depth is 0 or game is over

        if depth == 0 or len(self.b.get_all_legal_moves()) == 0:
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

    def change_notation(self, move):
        x1 = move[0][0]
        y1 = move[0][1]
        x2 = move[1][0]
        y2 = move[1][1]

        new_x1 = self.notation_dict_x[x1]
        new_y1 = self.notation_dict_y[y1]
        new_x2 = self.notation_dict_x[x2]
        new_y2 = self.notation_dict_y[y2]
        return "{}{}-{}{}".format(new_x1, new_y1, new_x2, new_y2)

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
            print(local_score, self.change_notation(move))
            self.b.pop(moved_piece, move[0])

        moved_piece = self.b.push(chosen_move)

        print(str(global_score) + " " + self.change_notation(chosen_move) + "\n")

        moved_piece = self.b.update_piece_pos2(moved_piece, chosen_move[1])

        with open("../data/cache.p", "wb") as cache:
            pickle.dump(self.board_caches, cache)
        return moved_piece
