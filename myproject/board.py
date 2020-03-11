# -*- coding: utf-8 -*-

import numpy as np
import piece as p


class Board:
    lu = 0  # upper limit
    ld = 7  # down limit

    def __init__(self, pieces):
        self.make_empty_board()
        self.fill_board(pieces)
        self.prev_board = self.board

    def make_empty_board(self):
        self.board = np.zeros((8, 8), dtype=object)

    def fill_board(self, pieces):
        for piece in pieces:
            self.place_piece(piece)

    def make_move(self, pos_start, pos_end):
        piece = self.board[pos_start[1], pos_start[0]]
        self.board[pos_end[1], pos_end[0]] = piece
        self.board[pos_start[1], pos_start[0]] = 0
        piece.pos = (pos_end[0], pos_end[1])
        return piece

    def get_pieces(self):
        return [piece for piece in self.board.reshape(64) if piece != 0]

    def get_king_pos(self, color):
        for piece in self.get_pieces():
            if isinstance(piece, p.King):
                if piece.color == color:
                    return piece.pos

    def place_piece(self, piece):
        self.board[piece.pos[1], piece.pos[0]] = piece

    def is_empty(self, pos):
        return self.board[pos[1], pos[0]] == 0

    def on_board(self, pos):
        return (
            (pos[0] >= self.lu)
            & (pos[0] <= self.ld)
            & (pos[1] >= self.lu)
            & (pos[1] <= self.ld)
        )

    def empty_on_board(self, pos):
        if self.on_board(pos):
            return self.is_empty(pos)
        else:
            return False

    def piece_color(self, pos):
        return self.board[pos[1], pos[0]].color
