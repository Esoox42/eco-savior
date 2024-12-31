"""
This file contains the UI class.
"""

import pygame
from config import *

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def render_ui(screen, player, game_time, font=None):
    if font is None:
        font = pygame.font.Font(None, 36)
    
    # Draw resources bar background
    resources_bar = pygame.Rect(0, 0, WINDOW_WIDTH, RESOURCES_BAR_HEIGHT)
    pygame.draw.rect(screen, (40, 40, 40), resources_bar)
    
    # Draw resources text
    resources_text = f"Money: {player.resources.money}  |  Energy: {player.resources.energy}  |  Waste: {player.resources.waste}  |  Happiness: {player.resources.happiness}"
    text = font.render(resources_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, RESOURCES_BAR_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Draw clock
    time_text = format_time(game_time)
    clock_text = font.render(time_text, True, (255, 255, 255))
    clock_rect = clock_text.get_rect(topright=(WINDOW_WIDTH - 20, 10))
    screen.blit(clock_text, clock_rect)