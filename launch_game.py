import pygame
from checkers.Visuals import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.GameSession import Game
from checkers.GameLogicAI import alpha_beta  

FPS = 60

# Initialize game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers Game')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def launch():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    game = Game(win)

    while run:
        clock.tick(FPS)

        if game.get_winner() is not None:
            print("Winner:", "WHITE" if game.get_winner() == WHITE else "RED")
            run = False

        if game.turn == WHITE:
            _, best_board = alpha_beta(game.get_board(), 4, float('-inf'), float('inf'), True, game)
            game.perform_ai_move(best_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.handle_selection(row, col)

        game.render()

    pygame.quit()

if __name__ == "__main__":
    launch()
