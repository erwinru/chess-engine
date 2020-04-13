# -*- coding: utf-8 -*-

import os

import pygame
from pygame.image import load

import board
import piece as p
import gui as g
import sys
import ai


class Game:
    def __init__(self, starting_player=True):

        self.is_player_white = starting_player
        pieces = self.create_pieces()
        b = board.Board(pieces)
        self.g = g.GUI(b)
        self.ai = ai.AI(b, self.is_player_white)
        self.game_loop(b)

    def create_pieces(self):
        ps = [
            p.Rook((0, 7), color=True, value=5, image=load("../images/w_rook.png")),
            p.Rook((7, 7), color=True, value=5, image=load("../images/w_rook.png")),
            p.Bishop((2, 7), color=True, value=3, image=load("../images/w_bishop.png")),
            p.Bishop((5, 7), color=True, value=3, image=load("../images/w_bishop.png")),
            p.Knight((1, 7), color=True, value=3, image=load("../images/w_knight.png")),
            p.Knight((6, 7), color=True, value=3, image=load("../images/w_knight.png")),
            p.Rook((0, 0), color=False, value=-5, image=load("../images/b_rook.png")),
            p.Rook((7, 0), color=False, value=-5, image=load("../images/b_rook.png")),
            p.Knight(
                (1, 0), color=False, value=-3, image=load("../images/b_knight.png")
            ),
            p.Knight(
                (6, 0), color=False, value=-3, image=load("../images/b_knight.png")
            ),
            p.Bishop(
                (2, 0), color=False, value=-3, image=load("../images/b_bishop.png")
            ),
            p.Bishop(
                (5, 0), color=False, value=-3, image=load("../images/b_bishop.png")
            ),
            p.King((4, 7), color=True, value=1000, image=load("../images/w_king.png")),
            p.Queen((3, 7), color=True, value=9, image=load("../images/w_queen.png")),
            p.King(
                (4, 0), color=False, value=-1000, image=load("../images/b_king.png")
            ),
            p.Queen((3, 0), color=False, value=-9, image=load("../images/b_queen.png")),
        ]
        for i in range(8):
            ps += [
                p.Pawn(
                    (i, 6),
                    color=True,
                    value=1,
                    image=pygame.image.load("../images/w_pawn.png"),
                ),
                p.Pawn(
                    (i, 1),
                    color=False,
                    value=-1,
                    image=pygame.image.load("../images/b_pawn.png"),
                ),
            ]
        return ps

    def get_board_pos(self, mx_pos, my_pos):
        x, y = mx_pos // 80, my_pos // 80
        return x, y

    def right_player(self, piece):
        return piece.color == self.is_player_white

    def change_curr_player(self):
        self.is_player_white = not self.is_player_white

    def check_king_or_rook_move(self, moved_piece):
        if isinstance(moved_piece, p.King) or isinstance(moved_piece, p.Rook):
            if not moved_piece.has_moved:
                moved_piece.has_moved = True

    def game_loop(self, b):

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if self.is_player_white:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mx_start, my_start = pygame.mouse.get_pos()
                        pos_start = self.get_board_pos(mx_start, my_start)
                        if not b.is_empty(pos_start):
                            moved_piece = b.board[-1][pos_start[1], pos_start[0]]

                    if event.type == pygame.MOUSEBUTTONUP:
                        mx_end, my_end = pygame.mouse.get_pos()
                        pos_end = self.get_board_pos(mx_end, my_end)
                        if (not b.is_empty(pos_start)) & self.right_player(moved_piece):
                            legal_moves = b.get_all_legal_moves()

                            move = [pos_start, pos_end]
                            if move in legal_moves:
                                moved_piece = b.push(move)
                                self.check_king_or_rook_move(moved_piece)
                                self.change_curr_player()
                                self.g.remake_board(b)
                            else:
                                print(
                                    "This move is not possible! Please make another move"
                                )
                else:
                    moved_piece = self.ai.move()
                    self.check_king_or_rook_move(moved_piece)
                    self.g.remake_board(b)
                    self.change_curr_player()


if __name__ == "__main__":
    Game()
