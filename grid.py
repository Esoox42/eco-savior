"""
This file contains the grid class.
"""

import pygame
from config import *
from infrastructure import *

class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = {}
        # Pre-calculate grid rects with offset
        self.grid_rects = [
            pygame.Rect(
                GRID_OFFSET_X + (x * CELL_SIZE),
                GRID_OFFSET_Y + (y * CELL_SIZE),
                CELL_SIZE,
                CELL_SIZE
            )
            for x in range(size)
            for y in range(size)
        ]

    def render(self, screen):
        # Draw grid background
        grid_background = pygame.Rect(
            GRID_OFFSET_X - 2,
            GRID_OFFSET_Y - 2,
            self.size * CELL_SIZE + 4,
            self.size * CELL_SIZE + 4
        )
        pygame.draw.rect(screen, (50, 50, 50), grid_background)
        
        # Draw grid lines (cached rects)
        for rect in self.grid_rects:
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
        
        # Draw infrastructure
        for (x, y), infrastructure in self.cells.items():
            rect = self.grid_rects[x * self.size + y]
            infrastructure.render(screen, rect)

    def build(self, x, y, infrastructure):
        if (x, y) not in self.cells:
            self.cells[(x, y)] = infrastructure
            return True
        return False