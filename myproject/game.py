# -*- coding: utf-8 -*-

import pygame
from pygame.image import load

import board as b
import piece as p
import gui as g
import sys


class Game:
    check = False

    def __init__(self, starting_player="w"):
        self.player_turn = starting_player
        pieces = self.create_pieces()
        board = b.Board(pieces)
        self.g = g.GUI(board)
        self.game_loop(board)

    def create_pieces(self):
        ps = [
            p.Rook((0, 7), color="w", image=load("images/w_rook.png")),
            p.Rook((7, 7), color="w", image=load("images/w_rook.png")),
            p.Bishop((2, 7), color="w", image=load("images/w_bishop.png")),
            p.Bishop((5, 7), color="w", image=load("images/w_bishop.png")),
            p.Knight((1, 7), color="w", image=load("images/w_knight.png")),
            p.Knight((6, 7), color="w", image=load("images/w_knight.png")),
            p.Rook((0, 0), color="b", image=load("images/b_rook.png")),
            p.Rook((7, 0), color="b", image=load("images/b_rook.png")),
            p.Knight((1, 0), color="b", image=load("images/b_knight.png")),
            p.Knight((6, 0), color="b", image=load("images/b_knight.png")),
            p.Bishop((2, 0), color="b", image=load("images/b_bishop.png")),
            p.Bishop((5, 0), color="b", image=load("images/b_bishop.png")),
            p.King((4, 7), color="w", image=load("images/w_king.png")),
            p.Queen((3, 7), color="w", image=load("images/w_queen.png")),
            p.King((4, 0), color="b", image=load("images/b_king.png")),
            p.Queen((3, 0), color="b", image=load("images/b_queen.png")),
        ]
        for i in range(8):
            ps += [
                p.Pawn((i, 6), color="w", image=pygame.image.load("images/w_pawn.png")),
                p.Pawn((i, 1), color="b", image=pygame.image.load("images/b_pawn.png")),
            ]
        return ps

    def possible_move(self, piece, b, pos_end):
        if pos_end in piece.possible_moves(b):
            return True

    def is_check(self, b):
        for piece in b.get_pieces():
            for move in piece.possible_moves(b):
                if move == b.get_king_pos(self.player_turn):
                    return True

    def move(self, b, pos_start, pos_end):
        b.prev_board = b.board.copy()
        piece = b.make_move(pos_start, pos_end)
        self.check_castled(b, piece, pos_start, pos_end)
        piece = self.check_pawn_prom(b, piece, pos_end)

    def check_castled(self, b, piece, pos_start, pos_end):
        if isinstance(piece, p.King):
            king = piece
            pos_diff = pos_start[0] - pos_end[0]
            # short castleing
            if pos_diff == -2:
                b.board[king.rel_pos(1, 0)[1], king.rel_pos(1, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(-1, 0),
                    color=king.color,
                    image=load("images/{}_rook.png".format(king.color)),
                )
                b.place_piece(rook)
            # long castleing
            elif pos_diff == 2:
                b.board[king.rel_pos(-2, 0)[1], king.rel_pos(-2, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(1, 0),
                    color=king.color,
                    image=load("images/{}_rook.png".format(king.color)),
                )
                b.place_piece(rook)
        if isinstance(piece, p.King) or isinstance(piece, p.Rook):
            if not piece.has_moved:
                piece.has_moved = True

    def check_pawn_prom(self, b, piece, pos_end):
        if isinstance(piece, p.Pawn):
            if (piece.color == "w") & (piece.pos[1] == b.lu):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    image=load("images/w_queen.png"),
                )
                b.place_piece(piece)
            elif (piece.color == "b") & (piece.pos[1] == b.ld):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    image=load("images/b_queen.png"),
                )
                b.place_piece(piece)
        return piece

    def get_board_pos(self, mx_pos, my_pos):
        x, y = mx_pos // 80, my_pos // 80
        return x, y

    def right_player(self, piece):
        return piece.color == self.player_turn

    def change_player_turn(self):
        if self.player_turn == "b":
            self.player_turn = "w"
        else:
            self.player_turn = "b"

    def game_loop(self, b):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx_start, my_start = pygame.mouse.get_pos()
                    pos_start = self.get_board_pos(mx_start, my_start)
                    if not b.is_empty(pos_start):
                        piece = b.board[pos_start[1], pos_start[0]]

                if event.type == pygame.MOUSEBUTTONUP:
                    mx_end, my_end = pygame.mouse.get_pos()
                    pos_end = self.get_board_pos(mx_end, my_end)
                    if (not b.is_empty(pos_start)) & self.right_player(piece):
                        if self.possible_move(piece, b, pos_end):
                            self.move(b, pos_start, pos_end)
                            if self.is_check(b):
                                print("Your king is check. Please make another move")
                                b.make_move(pos_end, pos_start)
                                b.board[b.board != b.prev_board] = b.prev_board[
                                    b.board != b.prev_board
                                ]
                            else:
                                self.change_player_turn()
                    self.g.remake_board(b)


if __name__ == "__main__":
    Game()
