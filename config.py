"""
This file contains the configuration for the game.
"""

GRID_SIZE = 4 # 4x4 grid
CELL_SIZE = 125 # 125x125 cell size
RESOURCES_BAR_HEIGHT = 50  # Height of the resources display bar
MENU_BAR_HEIGHT = 50      # Height of the bottom menu bar

# Window dimensions with padding
WINDOW_WIDTH = max(GRID_SIZE * CELL_SIZE + 100, 950)  # At least 950 wide
WINDOW_HEIGHT = RESOURCES_BAR_HEIGHT + (GRID_SIZE * CELL_SIZE) + MENU_BAR_HEIGHT + 75

# Calculate grid offset to center it
GRID_OFFSET_X = (WINDOW_WIDTH - (GRID_SIZE * CELL_SIZE)) // 2
GRID_OFFSET_Y = RESOURCES_BAR_HEIGHT + 25  # 25px padding below resources bar

FPS = 30
STARTING_MONEY = 1000
STARTING_ENERGY = 0
STARTING_WASTE = 0
STARTING_HAPPINESS = 50