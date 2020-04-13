# -*- coding: utf-8 -*-

import numpy as np
from pygame.image import load

import piece as p


class Board:
    ul = 0  # upper limit
    ll = 7  # lower limit
    notation_dict_x = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    notation_dict_y = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}

    def __init__(self, pieces):
        self.board = []  # treat board as a stack
        self.make_empty_board()
        self.fill_board(pieces)

    def make_empty_board(self):
        self.board.append(np.zeros((8, 8), dtype=object))

    def fill_board(self, pieces):
        for piece in pieces:
            self.place_piece(piece)

    def place_piece(self, piece):
        self.board[-1][piece.pos[1], piece.pos[0]] = piece

    def change_notation(self, pos):
        x = pos[0]
        y = pos[1]
        new_x = self.notation_dict_x[x]
        new_y = self.notation_dict_y[y]
        return (new_x, new_y)

    def full_move(self, pos_start, pos_end):
        board_x_start = pos_start[1]
        board_y_start = pos_start[0]
        board_x_end = pos_end[1]
        board_y_end = pos_end[0]

        curr_board = self.board[-1]

        moved_piece = curr_board[board_x_start, board_y_start]
        prev_board = curr_board.copy()
        curr_board[board_x_end, board_y_end] = moved_piece
        curr_board[board_x_start, board_y_start] = 0

        self.update_piece_pos2(moved_piece, pos_end)

        self.check_castled(moved_piece, pos_start, pos_end)
        self.check_pawn_prom(moved_piece, pos_end)
        return prev_board, moved_piece

    def restore_old_board(self, prev_board):
        self.board[-1][self.board[-1] != prev_board] = prev_board[
            self.board[-1] != prev_board
        ]

    def get_all_legal_moves(self):
        legal_moves = []
        for piece in self.get_pieces():
            if piece.color == self.get_curr_player():
                for pos_end in piece.possible_moves(self):
                    pos_start = piece.pos

                    # prev_board, moved_piece = self.full_move(pos_start, pos_end)

                    ###############
                    board_x_start = pos_start[1]
                    board_y_start = pos_start[0]
                    board_x_end = pos_end[1]
                    board_y_end = pos_end[0]

                    curr_board = self.board[-1]

                    moved_piece = curr_board[board_x_start, board_y_start]
                    prev_board = curr_board.copy()
                    curr_board[board_x_end, board_y_end] = moved_piece
                    curr_board[board_x_start, board_y_start] = 0

                    self.update_piece_pos2(moved_piece, pos_end)

                    self.check_castled(moved_piece, pos_start, pos_end)
                    self.check_pawn_prom(moved_piece, pos_end)
                    ############

                    if not self.is_check():
                        legal_moves.append([pos_start, pos_end])
                    self.restore_old_board(prev_board)

                    self.update_piece_pos2(moved_piece, pos_start)

        # legal_moves = np.array(legal_moves)
        #
        # result = [
        #     (self.change_notation(start_pos), self.change_notation(end_pos))
        #     for start_pos, end_pos in zip(legal_moves[:, 0], legal_moves[:, 1])
        # ]

        return legal_moves

    def update_piece_pos2(self, piece, new_pos):
        piece.pos = new_pos
        pass

    def print_piece_positions(self):
        for piece in self.get_pieces():
            print("{}: -- > {}".format(piece, self.change_notation(piece.pos)))

    def push(self, move):
        # prev_piece_pos = self.b.get_pieces()
        prev_board, moved_piece = self.full_move(move[0], move[1])
        self.board.append(self.board[-1])
        self.board[-2] = prev_board
        return moved_piece

    def pop(self, moved_piece, start_pos):
        self.board.pop()
        moved_piece.pos = start_pos

    def is_check(self):
        for piece in self.get_pieces():
            if piece.color != self.get_curr_player():
                for move_pos in piece.possible_moves(self):
                    if move_pos == self.get_king_pos():
                        return True

    def get_curr_player(self):
        if (len(self.board) % 2) == 0:
            return False
        else:
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
                self.board[-1][king.rel_pos(1, 0)[1], king.rel_pos(1, 0)[0]] = 0
                rook = p.Rook(
                    king.rel_pos(-1, 0),
                    color=king.color,
                    value=rook_value,
                    image=load("images/{}_rook.png".format(rook_color)),
                )
                self.place_piece(rook)
            # long castleing
            elif pos_diff == 2:
                self.board[-1][king.rel_pos(-2, 0)[1], king.rel_pos(-2, 0)[0]] = 0
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

    def get_pieces(self):
        return [field for field in self.board[-1].reshape(64) if field != 0]

    def get_king_pos(self):
        for piece in self.get_pieces():
            if isinstance(piece, p.King):
                if piece.color is self.get_curr_player():
                    return piece.pos

    def is_empty(self, pos):
        return self.board[-1][pos[1], pos[0]] == 0

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
        return self.board[-1][pos[1], pos[0]].color

    # def find_piece_coordinates(self, piece):
    #     for x in range(8):
    #         for y in range(8):
    #             if piece == self.board[-1][y, x]:
    #                 return (x, y)
    #
    # def update_piece_pos(self):
    #     for piece in self.get_pieces():
    #         if piece.pos != self.find_piece_coordinates(piece):
    #             moved_piece = piece
    #             piece.pos = self.find_piece_coordinates(piece)
    #             return moved_piece
