"""
This file contains the player class.
"""
from config import *
from resources import Resources

class Player:
    def __init__(self):
        self.resources = Resources(STARTING_MONEY, STARTING_ENERGY, STARTING_WASTE, STARTING_HAPPINESS)

    def spend_money(self, amount):
        if self.resources.money >= amount:
            self.resources.money -= amount
            return True
        return False

    def gain_money(self, amount):
        self.resources.money += amount
