
import pygame

from checkers.constants import width, height, square_size, red, white


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
    
   


main()