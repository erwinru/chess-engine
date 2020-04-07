# -*- coding: utf-8 -*-

import numpy as np
from pygame.image import load

import piece as p


class Board:
    ul = 0  # upper limit
    ll = 7  # lower limit

    def __init__(self, pieces):
        self.make_empty_board()
        self.fill_board(pieces)
        self.prev_board = self.board

    def make_empty_board(self):
        self.board = np.zeros((8, 8), dtype=object)

    def fill_board(self, pieces):
        for piece in pieces:
            self.place_piece(piece)

    def place_piece(self, piece):
        self.board[piece.pos[1], piece.pos[0]] = piece

    def make_move(self, pos_start, pos_end):
        piece = self.board[pos_start[1], pos_start[0]]
        self.board[pos_end[1], pos_end[0]] = piece
        self.board[pos_start[1], pos_start[0]] = 0
        piece.pos = (pos_end[0], pos_end[1])
        return piece

    def get_all_legal_moves(self, curr_player):
        legal_moves = []
        for piece in self.get_pieces():
            if piece.color == curr_player:
                for move_end_pos in piece.possible_moves(self):
                    start_pos = piece.pos
                    self.move(start_pos, move_end_pos)
                    if not self.is_check(curr_player):
                        legal_moves.append([start_pos, move_end_pos])
                    self.make_move(move_end_pos, start_pos)
                    self.board[self.board != self.prev_board] = self.prev_board[
                        self.board != self.prev_board
                    ]
        return legal_moves

    def get_child_positions(self):
        parent_position = self.board.copy()
        positions = []
        for move in self.get_all_legal_moves():
            self.move(move[0], move[1])
            positions += [self.board]
            self.make_move(move[1], move[0])
            self.board[self.board != parent_position] = self.prev_board[
                self.board != parent_position
            ]
        return positions, parent_position

    def is_check(self, curr_player):
        for piece in self.get_pieces():
            if piece.color != curr_player:
                for move_pos in piece.possible_moves(self):
                    if move_pos == self.get_king_pos(curr_player):
                        return True

    def move(self, pos_start, pos_end):
        self.prev_board = self.board.copy()
        piece = self.make_move(pos_start, pos_end)
        self.check_castled(piece, pos_start, pos_end)
        self.check_pawn_prom(piece, pos_end)
        return piece

    def check_castled(self, piece, pos_start, pos_end):
        if isinstance(piece, p.King):
            king = piece
            if king.color == "b":
                rook_value = -5
            else:
                rook_value = 5
            pos_diff = pos_start[0] - pos_end[0]
            # short castleing
            if pos_diff == -2:
                self.board[king.rel_pos(1, 0)[1], king.rel_pos(1, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(-1, 0),
                    color=king.color,
                    value=rook_value,
                    image=load("images/{}_rook.png".format(king.color)),
                )
                self.place_piece(rook)
            # long castleing
            elif pos_diff == 2:
                self.board[king.rel_pos(-2, 0)[1], king.rel_pos(-2, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(1, 0),
                    color=king.color,
                    value=rook_value,
                    image=load("images/{}_rook.png".format(king.color)),
                )
                self.place_piece(rook)

    def check_pawn_prom(self, piece, pos_end):
        if isinstance(piece, p.Pawn):
            if (piece.color == "w") & (piece.pos[1] == self.ul):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    image=load("images/w_queen.png"),
                )
                self.place_piece(piece)
            elif (piece.color == "b") & (piece.pos[1] == self.ll):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    image=load("images/b_queen.png"),
                )
                self.place_piece(piece)
        return piece

    def eval_board(self):
        return sum([piece.value for piece in self.get_pieces()])

    def get_pieces(self):
        return [field for field in self.board.reshape(64) if field != 0]

    def get_king_pos(self, color):
        for piece in self.get_pieces():
            if isinstance(piece, p.King):
                if piece.color == color:
                    return piece.pos

    def is_empty(self, pos):
        return self.board[pos[1], pos[0]] == 0

    def on_board(self, pos):
        return (
            (pos[0] >= self.ul)
            & (pos[0] <= self.ll)
            & (pos[1] >= self.ul)
            & (pos[1] <= self.ll)
        )

    def empty_on_board(self, pos):
        if self.on_board(pos):
            return self.is_empty(pos)
        else:
            return False

    def piece_color(self, pos):
        return self.board[pos[1], pos[0]].color
