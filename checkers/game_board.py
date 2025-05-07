import pygame
from .visuals import black, rows, red, square_size, cols, white
from .piece import Piece

class GameBoard:
    def __init__(self):
        self.grid = []
        self.red_pieces = self.white_pieces = 12
        self.red_kings = self.white_kings = 0
        self.setup_board()

    def draw_tiles(self, win):
        win.fill(black)
        for row in range(rows):
            for col in range(row % 2, cols, 2):
                pygame.draw.rect(win, red, (row * square_size, col * square_size, square_size, square_size))

    def score(self):
        return self.white_pieces - self.red_pieces + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def pieces_of_color(self, color):
        return [p for row in self.grid for p in row if p != 0 and p.color == color]

    def relocate(self, piece, new_row, new_col):
        self.grid[piece.row][piece.col], self.grid[new_row][new_col] = 0, piece
        piece.move(new_row, new_col)

        if new_row in [0, rows - 1]:
            piece.make_king()
            if piece.color == white:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def piece_at(self, row, col):
        return self.grid[row][col]

    def setup_board(self):
        for row in range(rows):
            self.grid.append([])
            for col in range(cols):
                if col % 2 == (row + 1) % 2:
                    if row < 3:
                        self.grid[row].append(Piece(row, col, white))
                    elif row > 4:
                        self.grid[row].append(Piece(row, col, red))
                    else:
                        self.grid[row].append(0)
                else:
                    self.grid[row].append(0)

    def render(self, win):
        self.draw_tiles(win)
        for row in range(rows):
            for col in range(cols):
                current = self.grid[row][col]
                if current != 0:
                    current.draw(win)

    def winner(self):
        if self.red_pieces <= 0:
            return white
        elif self.white_pieces <= 0:
            return red
        return None

    def available_moves(self, piece):
        valid = {}
        left, right = piece.col - 1, piece.col + 1
        row = piece.row

        if piece.color == red or piece.king:
            valid.update(self._scan_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            valid.update(self._scan_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == white or piece.king:
            valid.update(self._scan_left(row + 1, min(row + 3, rows), 1, piece.color, left))
            valid.update(self._scan_right(row + 1, min(row + 3, rows), 1, piece.color, right))

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
                    limit = max(r - 3, 0) if step == -1 else min(r + 3, rows)
                    moves.update(self._scan_left(r + step, limit, step, color, col - 1, skipped=temp))
                    moves.update(self._scan_right(r + step, limit, step, color, col + 1, skipped=temp))
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
            if col >= cols:
                break
            spot = self.grid[r][col]
            if spot == 0:
                if jumped and not temp:
                    break
                moves[(r, col)] = temp + jumped if jumped else temp
                if temp:
                    limit = max(r - 3, 0) if step == -1 else min(r + 3, rows)
                    moves.update(self._scan_left(r + step, limit, step, color, col - 1, skipped=temp))
                    moves.update(self._scan_right(r + step, limit, step, color, col + 1, skipped=temp))
                break
            elif spot.color == color:
                break
            else:
                temp = [spot]
            col += 1
        return moves
