# -*- coding: utf-8 -*-

import pygame
from pygame.image import load

import board
import piece as p
import gui as g
import sys
import ai


class Game:
    notation_dict_x = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    notation_dict_y = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

    def __init__(self, starting_player=True):
        self.curr_player = starting_player
        pieces = self.create_pieces()
        b = board.Board(pieces)
        self.g = g.GUI(b)
        self.ai = ai.AI(b)
        self.game_loop(b)

    def create_pieces(self):
        ps = [
            p.Rook((0, 7), color=True, value=5, image=load("images/w_rook.png")),
            p.Rook((7, 7), color=True, value=5, image=load("images/w_rook.png")),
            p.Bishop((2, 7), color=True, value=3, image=load("images/w_bishop.png")),
            p.Bishop((5, 7), color=True, value=3, image=load("images/w_bishop.png")),
            p.Knight((1, 7), color=True, value=3, image=load("images/w_knight.png")),
            p.Knight((6, 7), color=True, value=3, image=load("images/w_knight.png")),
            p.Rook((0, 0), color=False, value=-5, image=load("images/b_rook.png")),
            p.Rook((7, 0), color=False, value=-5, image=load("images/b_rook.png")),
            p.Knight((1, 0), color=False, value=-3, image=load("images/b_knight.png")),
            p.Knight((6, 0), color=False, value=-3, image=load("images/b_knight.png")),
            p.Bishop((2, 0), color=False, value=-3, image=load("images/b_bishop.png")),
            p.Bishop((5, 0), color=False, value=-3, image=load("images/b_bishop.png")),
            p.King((4, 7), color=True, value=1000, image=load("images/w_king.png")),
            p.Queen((3, 7), color=True, value=9, image=load("images/w_queen.png")),
            p.King((4, 0), color=False, value=-1000, image=load("images/b_king.png")),
            p.Queen((3, 0), color=False, value=-9, image=load("images/b_queen.png")),
        ]
        for i in range(8):
            ps += [
                p.Pawn(
                    (i, 6),
                    color=True,
                    value=1,
                    image=pygame.image.load("images/w_pawn.png"),
                ),
                p.Pawn(
                    (i, 1),
                    color=False,
                    value=-1,
                    image=pygame.image.load("images/b_pawn.png"),
                ),
            ]
        return ps

    def get_board_pos(self, mx_pos, my_pos):
        x, y = mx_pos // 80, my_pos // 80
        return x, y

    def right_player(self, piece):
        return piece.color == self.curr_player

    def change_curr_player(self):
        if self.curr_player is False:
            self.curr_player = True
        else:
            self.curr_player = False

    def change_notation(self, pos):
        x = pos[0]
        y = pos[1]
        new_x = self.notation_dict_x[x]
        new_y = self.notation_dict_y[y]
        return (new_x, new_y)

    def game_loop(self, b):

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if self.curr_player:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx_start, my_start = pygame.mouse.get_pos()
                        pos_start = self.get_board_pos(mx_start, my_start)
                        if not b.is_empty(pos_start):
                            moved_piece = b.board[pos_start[1], pos_start[0]]

                    if event.type == pygame.MOUSEBUTTONUP:
                        mx_end, my_end = pygame.mouse.get_pos()
                        pos_end = self.get_board_pos(mx_end, my_end)
                        if (not b.is_empty(pos_start)) & self.right_player(moved_piece):
                            legal_moves = b.get_all_legal_moves(
                                b.board, self.curr_player
                            )
                            # print(legal_moves)
                            move = [pos_start, pos_end]
                            if move in legal_moves:
                                piece = b.full_move(b.board, pos_start, pos_end)
                                if isinstance(piece, p.King) or isinstance(
                                    piece, p.Rook
                                ):
                                    if not piece.has_moved:
                                        piece.has_moved = True
                                self.change_curr_player()
                                self.g.remake_board(b)
                            else:
                                print(
                                    "This move is not possible! Please make another move"
                                )
                else:
                    ai_calculating_board = b.board.copy()
                    best_eval = self.ai.minimax(
                        position=ai_calculating_board, depth=2, maximizingPlayer=False
                    )
                    # from IPython import embed
                    #
                    # embed()
                    new_position, moved_piece = self.ai.move(
                        best_eval, self.curr_player, ai_calculating_board
                    )
                    if isinstance(piece, p.King) or isinstance(piece, p.Rook):
                        if not piece.has_moved:
                            piece.has_moved = True
                    self.change_curr_player()
                    self.g.remake_board(b)


if __name__ == "__main__":
    Game()
