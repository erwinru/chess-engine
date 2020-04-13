# -*- coding: utf-8 -*-

import pygame


class GUI:
    SQ_LEN = 80

    GRAY_LIGHT = (240, 240, 240)
    GRAY_DARK = (200, 200, 200)

    BOARD_COLOR = (GRAY_LIGHT, GRAY_DARK)

    def __init__(self, b):
        pygame.init()
        self.make_window()
        self.make_empty_board()
        self.fill_board(b)
        pygame.display.flip()

    def make_window(self):
        self.win = pygame.display.set_mode((8 * self.SQ_LEN, 8 * self.SQ_LEN))
        pygame.display.set_caption("Chess")

    def make_empty_board(self):
        self.win.fill(self.BOARD_COLOR[0])
        self.fill_dark_squares()

    def fill_dark_squares(self):
        for x, y in self.dark_sq_pos():
            self.draw_square(x, y, self.BOARD_COLOR[1])

    def dark_sq_pos(self):
        for i in range(8):
            for j in range(8):
                if self.check_dark(i, j):
                    yield (i, j)

    def check_dark(self, x, y):
        return (x + y + 2) % 2 == 1

    def draw_square(self, x, y, color):
        pygame.draw.rect(
            self.win,
            color,
            (x * self.SQ_LEN, y * self.SQ_LEN, self.SQ_LEN, self.SQ_LEN),
            0,
        )

    def fill_board(self, b):
        for piece in b.get_pieces():
            self.win.blit(
                pygame.transform.scale(piece.image, (self.SQ_LEN, self.SQ_LEN)),
                pygame.Rect(
                    ((piece.pos[0]) * self.SQ_LEN, (piece.pos[1]) * self.SQ_LEN),
                    (self.SQ_LEN, self.SQ_LEN),
                ),
            )

    def remake_board(self, b):
        self.make_empty_board()
        self.fill_board(b)
        pygame.display.flip()

    def update_move(self, piece, start, end):
        self.make_empty(start, end)
        self.place_image(piece)
        pygame.display.flip()

    def place_image(self, piece):
        self.win.blit(
            pygame.transform.scale(piece.image, (self.SQ_LEN, self.SQ_LEN)),
            pygame.Rect(
                ((piece.pos[0]) * self.SQ_LEN, (piece.pos[1]) * self.SQ_LEN),
                (self.SQ_LEN, self.SQ_LEN),
            ),
        )

    def make_empty(self, start_pos, end_pos):
        for pos in (start_pos, end_pos):
            if self.check_dark(*pos):
                self.draw_square(*pos, self.BOARD_COLOR[1])
            else:
                self.draw_square(*pos, self.BOARD_COLOR[0])
