"""
This file contains the infrastructure class.
"""

import pygame

class Infrastructure:
    def __init__(self, name, cost, energy_usage, waste_production):
        self.name = name
        self.cost = cost
        self.energy_usage = energy_usage
        self.waste_production = waste_production

    def render(self, screen, rect):
        pygame.draw.rect(screen, (0, 128, 0), rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (rect.x + 5, rect.y + 5))

class EnergyPlant(Infrastructure):
    def __init__(self):
        super().__init__("Energy Plant", 500, -100, 50)

class WasteFactory(Infrastructure):
    def __init__(self):
        super().__init__("Waste Factory", 700, 50, -50)

class House(Infrastructure):
    def __init__(self):
        super().__init__("House", 300, 50, 20)