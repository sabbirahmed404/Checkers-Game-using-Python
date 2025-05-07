import pygame
import time
import random
from copy import deepcopy

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minimax Visualization')
FONT = pygame.font.SysFont('comicsans', 20)

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(win, self.color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                            self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius)
        if self.king:
            text = FONT.render('K', 1, BLACK)
            win.blit(text, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2, 
                           self.row * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2))

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        
    def create_board(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row][col] = Piece(row, col, WHITE)
                    elif row > 4:
                        self.board[row][col] = Piece(row, col, RED)
                    else:
                        self.board[row][col] = 0
                else:
                    self.board[row][col] = 0
    
    def draw(self, win, current_search=None):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        
        # Highlight current search position
        if current_search:
            row, col = current_search
            pygame.draw.rect(win, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, GRAY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
    
    def get_all_pieces(self, color):
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    pieces.append(self.board[row][col])
        return pieces
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.row, piece.col = row, col
        
        # Make king if reached end
        if row == 0 and piece.color == RED:
            piece.king = True
            self.red_kings += 1
        elif row == ROWS - 1 and piece.color == WHITE:
            piece.king = True
            self.white_kings += 1
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

def minimax(position, depth, max_player, game, win):
    """Minimax algorithm with visualization"""
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    
    # Visualize the search
    position.draw(win)
    pygame.display.update()
    time.sleep(0.1)  # Slow down to see the search
    
    if max_player:  # WHITE's turn (maximizing)
        max_eval = float('-inf')
        best_move = None
        
        for piece in position.get_all_pieces(WHITE):
            # Visualize current piece being considered
            position.draw(win, (piece.row, piece.col))
            pygame.display.update()
            time.sleep(0.2)
            
            # Simple moves for demo (just random valid moves)
            possible_moves = get_simple_moves(position, piece)
            
            for move in possible_moves:
                row, col = move
                # Create a simulation of this move
                temp_board = deepcopy(position)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                temp_board.move(temp_piece, row, col)
                
                # Recursively evaluate this move
                eval, _ = minimax(temp_board, depth-1, False, game, win)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = temp_board
        
        return max_eval, best_move
    
    else:  # RED's turn (minimizing)
        min_eval = float('inf')
        best_move = None
        
        for piece in position.get_all_pieces(RED):
            # Visualize current piece being considered
            position.draw(win, (piece.row, piece.col))
            pygame.display.update()
            time.sleep(0.2)
            
            # Simple moves for demo
            possible_moves = get_simple_moves(position, piece)
            
            for move in possible_moves:
                row, col = move
                # Create a simulation of this move
                temp_board = deepcopy(position)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                temp_board.move(temp_piece, row, col)
                
                # Recursively evaluate this move
                eval, _ = minimax(temp_board, depth-1, True, game, win)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = temp_board
        
        return min_eval, best_move

def get_simple_moves(board, piece):
    """Simplified move generation for demo purposes"""
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dr, dc in directions:
        new_row, new_col = piece.row + dr, piece.col + dc
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and board.board[new_row][new_col] == 0:
            moves.append((new_row, new_col))
    
    # Return a subset of moves for visualization purposes
    return moves[:min(2, len(moves))]

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Run minimax with visualization when space is pressed
                    value, new_board = minimax(board, 3, True, None, WIN)
                    if new_board:
                        board = new_board
        
        board.draw(WIN)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()