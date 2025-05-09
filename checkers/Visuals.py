

import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# RGB Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Additional colors for game session
TONE_RED = RED
TONE_WHITE = WHITE
HINT_BLUE = BLUE
CELL_SIZE = SQUARE_SIZE

# Load crown image
CROWN = pygame.transform.scale(pygame.image.load('assets/crown1.jpg'), (44, 25))
