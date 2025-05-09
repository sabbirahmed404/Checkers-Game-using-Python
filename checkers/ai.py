
from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def alpha_beta(position, depth, alpha, beta, maximizing_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation, _ = alpha_beta(move, depth - 1, alpha, beta, False, game)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Prune
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation, _ = alpha_beta(move, depth - 1, alpha, beta, True, game)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Prune
        return min_eval, best_move

def simulate_move(piece, move, board, game, skip):
    board.relocate(piece, move[0], move[1])
    if skip:
        board.eliminate(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    for piece in board.pieces_of_color(color):
        valid_moves = board.available_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.piece_at(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves
