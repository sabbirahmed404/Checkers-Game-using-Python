# visuals.py

import pygame

# Display configuration
DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 800
GRID_ROWS, GRID_COLS = 8, 8
CELL_SIZE = DISPLAY_WIDTH // GRID_COLS

# Color palette
TONE_RED = (255, 0, 0)
TONE_WHITE = (255, 255, 255)
TONE_BLACK = (0, 0, 0)
TONE_BLUE = (0, 0, 255)
TONE_GREY = (128, 128, 128)

# Load and scale the king icon
KING_ICON = pygame.transform.scale(
    pygame.image.load("assests/crown1.jpg"), (44, 25)
)
