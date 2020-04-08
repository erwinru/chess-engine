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

    def full_move(self, parent_position, pos_start, pos_end):
        self.prev_board = self.board.copy()
        piece = parent_position[pos_start[1], pos_start[0]]
        self.prev_piece_pos = piece.pos
        parent_position[pos_end[1], pos_end[0]] = piece
        parent_position[pos_start[1], pos_start[0]] = 0
        piece.pos = (pos_end[0], pos_end[1])

        self.check_castled(piece, pos_start, pos_end)
        self.check_pawn_prom(piece, pos_end)
        return piece

    def get_all_possible_moves(self, parent_position, curr_player):
        possible_moves = []
        for piece in self.get_pieces(parent_position):
            if piece.color == curr_player:
                for move_end_pos in piece.possible_moves(self):
                    start_pos = piece.pos
                    possible_moves.append([piece, start_pos, move_end_pos])
        return possible_moves

    def get_all_legal_moves(self, parent_position, curr_player):
        legal_moves = []
        for piece in self.get_pieces(parent_position):
            if piece.color == curr_player:
                for move_end_pos in piece.possible_moves(self):
                    start_pos = piece.pos
                    self.full_move(parent_position, start_pos, move_end_pos)
                    if not self.is_check(parent_position, curr_player):
                        legal_moves.append([start_pos, move_end_pos])
                    self.board[self.board != self.prev_board] = self.prev_board[
                        self.board != self.prev_board
                    ]
                    piece.pos = self.prev_piece_pos
        return legal_moves

    def get_child_positions(self, parent_position, curr_player):
        # parent_position = self.board.copy()
        child_positions = []
        for move in self.get_all_legal_moves(parent_position, curr_player):
            piece = parent_position[move[0][1], move[0][0]]
            prev_piece_pos = piece.pos
            self.full_move(parent_position, move[0], move[1])
            child_positions += [self.board.copy()]
            self.board[self.board != self.prev_board] = self.prev_board[
                self.board != self.prev_board
            ]
            piece.pos = prev_piece_pos
        return child_positions

    def is_check(self, position, curr_player):
        for piece in self.get_pieces(position):
            if piece.color != curr_player:
                for move_pos in piece.possible_moves(self):
                    if move_pos == self.get_king_pos(position, curr_player):
                        return True

    def check_castled(self, piece, pos_start, pos_end):
        if isinstance(piece, p.King):
            king = piece
            if king.color is False:
                rook_value = -5
                rook_color = "b"
            else:
                rook_value = 5
                rook_color = "w"
            pos_diff = pos_start[0] - pos_end[0]
            # short castleing
            if pos_diff == -2:
                self.board[king.rel_pos(1, 0)[1], king.rel_pos(1, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(-1, 0),
                    color=king.color,
                    value=rook_value,
                    image=load("images/{}_rook.png".format(rook_color)),
                )
                self.place_piece(rook)
            # long castleing
            elif pos_diff == 2:
                self.board[king.rel_pos(-2, 0)[1], king.rel_pos(-2, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(1, 0),
                    color=king.color,
                    value=rook_value,
                    image=load("images/{}_rook.png".format(rook_color)),
                )
                self.place_piece(rook)

    def check_pawn_prom(self, piece, pos_end):
        if isinstance(piece, p.Pawn):
            if (piece.color is True) & (piece.pos[1] == self.ul):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    value=9,
                    image=load("images/w_queen.png"),
                )
                self.place_piece(piece)
            elif (piece.color is False) & (piece.pos[1] == self.ll):
                piece = p.Queen(
                    (pos_end[0], pos_end[1]),
                    color=piece.color,
                    value=-9,
                    image=load("images/b_queen.png"),
                )
                self.place_piece(piece)
        return piece

    def get_pieces(self, position):
        return [field for field in position.reshape(64) if field != 0]

    def get_king_pos(self, position, color):
        for piece in self.get_pieces(position):
            if isinstance(piece, p.King):
                if piece.color is color:
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

    def find_board_coordinates(self, piece):
        for x in range(8):
            for y in range(8):
                if piece == self.board[y, x]:
                    return (x, y)
