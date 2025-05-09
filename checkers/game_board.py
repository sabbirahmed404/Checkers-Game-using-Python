import pygame
from .Visuals import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class GameBoard:
    def __init__(self):
        self.grid = []
        self.red_pieces = self.white_pieces = 12
        self.red_kings = self.white_kings = 0
        self.setup_board()

    def draw_tiles(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def score(self):
        return self.white_pieces - self.red_pieces + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def evaluate(self):
        return self.score()

    def pieces_of_color(self, color):
        return [p for row in self.grid for p in row if p != 0 and p.color == color]

    def relocate(self, piece, new_row, new_col):
        self.grid[piece.row][piece.col], self.grid[new_row][new_col] = 0, piece
        piece.move(new_row, new_col)

        if new_row in [0, ROWS - 1]:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def piece_at(self, row, col):
        return self.grid[row][col]

    def eliminate(self, pieces):
        for piece in pieces:
            self.grid[piece.row][piece.col] = 0
            if piece.color == RED:
                self.red_pieces -= 1
            else:
                self.white_pieces -= 1

    def setup_board(self):
        for row in range(ROWS):
            self.grid.append([])
            for col in range(COLS):
                if col % 2 == (row + 1) % 2:
                    if row < 3:
                        self.grid[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.grid[row].append(Piece(row, col, RED))
                    else:
                        self.grid[row].append(0)
                else:
                    self.grid[row].append(0)

    def render(self, win):
        self.draw_tiles(win)
        for row in range(ROWS):
            for col in range(COLS):
                current = self.grid[row][col]
                if current != 0:
                    current.draw(win)

    def winner(self):
        if self.red_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return RED
        return None

    def available_moves(self, piece):
        valid = {}
        left, right = piece.col - 1, piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            valid.update(self._scan_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            valid.update(self._scan_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            valid.update(self._scan_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            valid.update(self._scan_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return valid

    def _scan_left(self, start, stop, step, color, col, jumped=[]):
        moves, temp = {}, []
        for r in range(start, stop, step):
            if col < 0:
                break
            spot = self.grid[r][col]
            if spot == 0:
                if jumped and not temp:
                    break
                moves[(r, col)] = temp + jumped if jumped else temp
                if temp:
                    limit = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._scan_left(r + step, limit, step, color, col - 1, jumped=temp))
                    moves.update(self._scan_right(r + step, limit, step, color, col + 1, jumped=temp))
                break
            elif spot.color == color:
                break
            else:
                temp = [spot]
            col -= 1
        return moves

    def _scan_right(self, start, stop, step, color, col, jumped=[]):
        moves, temp = {}, []
        for r in range(start, stop, step):
            if col >= COLS:
                break
            spot = self.grid[r][col]
            if spot == 0:
                if jumped and not temp:
                    break
                moves[(r, col)] = temp + jumped if jumped else temp
                if temp:
                    limit = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._scan_left(r + step, limit, step, color, col - 1, jumped=temp))
                    moves.update(self._scan_right(r + step, limit, step, color, col + 1, jumped=temp))
                break
            elif spot.color == color:
                break
            else:
                temp = [spot]
            col += 1
        return moves
