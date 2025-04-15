
import pygame

from checkers.constants import width, height, square_size, red, white
from checkers.game import Game
from minimax.algorithm import minimax


fps = 60

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(win)

    while run:
        clock.tick(fps)

        if game.turn == white:
            value, new_board = minimax(game.get_board(), 4, white, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

    
   
   
main()