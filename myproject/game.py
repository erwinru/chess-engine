# -*- coding: utf-8 -*-

import pygame
from pygame.image import load

import board
import piece as p
import gui as g
import sys


class Game:
    check = False
    notation_dict_x = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    notation_dict_y = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

    def __init__(self, starting_player="w"):
        self.curr_player_color = starting_player
        pieces = self.create_pieces()
        self.b = board.Board(pieces)
        self.g = g.GUI(self.b)
        self.game_loop()

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

    def check_possible_move(self, piece, pos_end):
        if pos_end in piece.possible_moves(self.b):
            return True

    def is_check(self):
        for piece in self.b.get_pieces():
            if piece.color != self.curr_player_color:
                for move_pos in piece.possible_moves(self.b):
                    if move_pos == self.b.get_king_pos(self.curr_player_color):
                        return True

    def move(self, pos_start, pos_end):
        self.b.prev_board = self.b.board.copy()
        piece = self.b.make_move(pos_start, pos_end)
        self.check_castled(piece, pos_start, pos_end)
        piece = self.check_pawn_prom(piece, pos_end)

    def check_castled(self, piece, pos_start, pos_end):
        if isinstance(piece, p.King):
            king = piece
            pos_diff = pos_start[0] - pos_end[0]
            # short castleing
            if pos_diff == -2:
                self.b.board[king.rel_pos(1, 0)[1], king.rel_pos(1, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(-1, 0),
                    color=king.color,
                    image=load("images/{}_rook.png".format(king.color)),
                )
                self.b.place_piece(rook)
            # long castleing
            elif pos_diff == 2:
                self.b.board[king.rel_pos(-2, 0)[1], king.rel_pos(-2, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(1, 0),
                    color=king.color,
                    image=load("images/{}_rook.png".format(king.color)),
                )
                self.b.place_piece(rook)
        if isinstance(piece, p.King) or isinstance(piece, p.Rook):
            if not piece.has_moved:
                piece.has_moved = True

    def check_pawn_prom(self, piece, pos_end):
        if isinstance(piece, p.Pawn):
            if (piece.color == "w") & (piece.pos[1] == self.b.ul):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    image=load("images/w_queen.png"),
                )
                self.b.place_piece(piece)
            elif (piece.color == "b") & (piece.pos[1] == self.b.ll):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    image=load("images/b_queen.png"),
                )
                self.b.place_piece(piece)
        return piece

    def get_board_pos(self, mx_pos, my_pos):
        x, y = mx_pos // 80, my_pos // 80
        return x, y

    def right_player(self, piece):
        return piece.color == self.curr_player_color

    def change_curr_player_color(self):
        if self.curr_player_color == "b":
            self.curr_player_color = "w"
        else:
            self.curr_player_color = "b"

    def change_notation(self, pos):
        x = pos[0]
        y = pos[1]
        new_x = self.notation_dict_x[x]
        new_y = self.notation_dict_y[y]
        return (new_x, new_y)

    def print_all_possible_moves(self):
        for piece in self.b.get_pieces():
            if piece.color == self.curr_player_color:
                print("{} {}:".format(piece.color, piece.name))
                for move_pos in piece.possible_moves(self.b):
                    print("{}".format(self.change_notation(move_pos)))
                print("\n")

    def game_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx_start, my_start = pygame.mouse.get_pos()
                    pos_start = self.get_board_pos(mx_start, my_start)
                    if not self.b.is_empty(pos_start):
                        moved_piece = self.b.board[pos_start[1], pos_start[0]]

                if event.type == pygame.MOUSEBUTTONUP:
                    self.print_all_possible_moves()
                    mx_end, my_end = pygame.mouse.get_pos()
                    pos_end = self.get_board_pos(mx_end, my_end)
                    if (not self.b.is_empty(pos_start)) & self.right_player(
                        moved_piece
                    ):
                        if self.check_possible_move(moved_piece, pos_end):
                            self.move(pos_start, pos_end)
                            if self.is_check():
                                print(
                                    "This move is not possible. Your king is check. Please make another move"
                                )
                                self.b.make_move(pos_end, pos_start)
                                self.b.board[
                                    self.b.board != self.b.prev_board
                                ] = self.b.prev_board[self.b.board != self.b.prev_board]
                            else:
                                self.change_curr_player_color()
                    self.g.remake_board(self.b)


if __name__ == "__main__":
    Game()
