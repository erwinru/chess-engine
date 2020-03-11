# -*- coding: utf-8 -*-
import itertools


class Piece:
    def __init__(self, start_pos, color, image):
        self.pos = start_pos
        self.color = color
        self.image = image

    def rel_pos(self, rel_x, rel_y):
        return (self.pos[0] + rel_x, self.pos[1] + rel_y)

    def diff_color(self, board, pos):
        return self.color != board.piece_color(pos)

    def move_line(self, b, _range, orientation):
        m = []
        for ori in ("h", "v"):
            for direction in (+1, -1):
                start = direction * (b.lu + 1)
                stop = direction * (_range + 1)
                step = direction
                for j in range(start, stop, step):
                    if orientation == "diagonal":
                        if ori == "v":
                            pos = self.rel_pos(j, j)
                        elif ori == "h":
                            pos = self.rel_pos(-j, j)
                    elif orientation == "straight":
                        if ori == "v":
                            pos = self.rel_pos(0, j)
                        elif ori == "h":
                            pos = self.rel_pos(j, 0)
                    if b.on_board(pos):
                        if b.is_empty(pos):
                            m.append(pos)
                        else:
                            if self.diff_color(b, pos):
                                m.append(pos)
                            break
                    else:
                        break
        return m


class Pawn(Piece):
    def possible_moves(self, b):
        m = []
        # moving
        if self.color == "w":
            dir = -1
            start_line = 6
        elif self.color == "b":
            dir = +1
            start_line = 1
        if b.empty_on_board(self.rel_pos(0, dir * 1)):
            m.append(self.rel_pos(0, dir * 1))
            if (b.empty_on_board(self.rel_pos(0, dir * 2))) & (
                self.pos[1] == start_line
            ):
                m.append(self.rel_pos(0, dir * 2))
        # capturing
        for pos in ((-1, dir * 1), ((1, dir * 1))):
            if b.on_board(self.rel_pos(*pos)):
                if not b.is_empty(self.rel_pos(*pos)):
                    if self.diff_color(b, self.rel_pos(*pos)):
                        m.append(self.rel_pos(*pos))
        return m

    def __repr__(self):
        return "P_{}".format(self.color)


class Rook(Piece):
    def __init__(self, start_pos, color, image, has_moved=False):
        super().__init__(start_pos, color, image)
        self.has_moved = has_moved

    def possible_moves(self, b):
        return self.move_line(b, _range=b.ld, orientation="straight")

    def __repr__(self):
        return "R_{}".format(self.color)


class Knight(Piece):
    def possible_moves(self, b):
        comb = itertools.permutations((1, -1, 2, -2), 2)
        rel_poss = [x for x in comb if sum([abs(x[0]), abs(x[1])]) == 3]
        m = []
        for rel_pos in rel_poss:
            pos = self.rel_pos(*rel_pos)
            if b.on_board(pos):
                if b.is_empty(pos):
                    m.append(pos)
                else:
                    if self.diff_color(b, pos):
                        m.append(pos)
        return m

    def __repr__(self):
        return "Kn_{}".format(self.color)


class Bishop(Piece):
    def possible_moves(self, b):
        return self.move_line(b, _range=b.ld, orientation="diagonal")

    def __repr__(self):
        return "B_{}".format(self.color)


class Queen(Piece):
    def possible_moves(self, b):
        m = []
        m += self.move_line(b, _range=b.ld, orientation="diagonal")
        m += self.move_line(b, _range=b.ld, orientation="straight")
        return m

    def __repr__(self):
        return "Q_{}".format(self.color)


class King(Piece):
    def __init__(self, start_pos, color, image, has_moved=False):
        super().__init__(start_pos, color, image)
        self.has_moved = has_moved

    def possible_moves(self, b):
        m = []
        m += self.move_line(b, _range=1, orientation="diagonal")
        m += self.move_line(b, _range=1, orientation="straight")
        if self.short_castleing(b):
            m.append(self.rel_pos(2, 0))
        if self.long_castleing(b):
            m.append(self.rel_pos(-2, 0))
        return m

    def short_castleing(self, b):
        if not self.has_moved:
            if b.is_empty(self.rel_pos(1, 0)) & b.is_empty(self.rel_pos(2, 0)):
                if isinstance(
                    b.board[self.rel_pos(3, 0)[1], self.rel_pos(3, 0)[0]], Rook
                ):
                    if not b.board[
                        self.rel_pos(3, 0)[1], self.rel_pos(3, 0)[0]
                    ].has_moved:
                        return True
        return False

    def long_castleing(self, b):
        if (
            b.is_empty(self.rel_pos(-1, 0))
            & b.is_empty(self.rel_pos(-2, 0))
            & b.is_empty(self.rel_pos(-3, 0))
        ):
            if isinstance(
                b.board[self.rel_pos(-4, 0)[1], self.rel_pos(-4, 0)[0]], Rook
            ):
                if not b.board[
                    self.rel_pos(-4, 0)[1], self.rel_pos(-4, 0)[0]
                ].has_moved:
                    return True

    def __repr__(self):
        return "K_{}".format(self.color)
