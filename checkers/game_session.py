import pygame
from .Visuals import TONE_RED, TONE_WHITE, HINT_BLUE, CELL_SIZE, RED, WHITE
from .game_board import GameBoard

class GameSession:
    def __init__(self, display_surface):
        self.screen = display_surface
        self._initialize_session()

    def _initialize_session(self):
        self.focused_piece = None
        self.grid = GameBoard()
        self.active_player = TONE_RED
        self.turn = TONE_RED
        self.highlight_map = {}

    def update(self):
        self.grid.render(self.screen)
        self._highlight_moves(self.highlight_map)
        pygame.display.flip()

    def reset_game(self):
        self._initialize_session()

    def get_board(self):
        return self.grid

    def ai_move(self, new_state):
        self.grid = new_state
        self._toggle_player()

    def winner(self):
        return self.grid.winner()

    def select(self, r, c):
        if self.focused_piece:
            if not self._attempt_move(r, c):
                self.focused_piece = None
                self.select(r, c)
            return

        piece = self.grid.piece_at(r, c)
        if piece != 0 and piece.color == self.active_player:
            self.focused_piece = piece
            self.highlight_map = self.grid.available_moves(piece)

    def _attempt_move(self, r, c):
        if self.focused_piece is None:
            return False

        target_cell = self.grid.piece_at(r, c)
        if target_cell == 0 and (r, c) in self.highlight_map:
            self.grid.relocate(self.focused_piece, r, c)
            eliminated = self.highlight_map[(r, c)]
            if eliminated:
                for piece in eliminated:
                    self.grid.grid[piece.row][piece.col] = 0
                    if piece.color == RED:
                        self.grid.red_pieces -= 1
                    else:
                        self.grid.white_pieces -= 1
            self._toggle_player()
            return True

        return False

    def _highlight_moves(self, moveset):
        for pos in moveset:
            r, c = pos
            pygame.draw.circle(
                self.screen,
                HINT_BLUE,
                (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2),
                15
            )

    def _toggle_player(self):
        self.highlight_map = {}
        self.active_player = TONE_WHITE if self.active_player == TONE_RED else TONE_RED
        self.turn = self.active_player
