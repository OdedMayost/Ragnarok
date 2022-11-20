import pygame
import os

TRANSPARENT_COLOR = (250, 0, 250)


class Life(pygame.sprite.Sprite):
    def __init__(self, screen, x_pos, y_pos):
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.heart_life = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\Life\\HeartLife.png")
        self.heart_life.set_colorkey(TRANSPARENT_COLOR)
        self.heart_half_life = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\Life\\HeartHalfLife.png")
        self.heart_half_life.set_colorkey(TRANSPARENT_COLOR)
        self.heart_death = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\Life\\HeartDeath.png")
        self.heart_death.set_colorkey(TRANSPARENT_COLOR)
        self.hearts = 3 * 2
        self.screen = screen

    def remove_life(self, player_type):
        if player_type == "HeartHalfLife":
            self.hearts -= 1
        elif player_type == "HeartDeath":
            self.hearts -= 2

    def print_life(self):
        amount_hearts = self.hearts
        max_hearts = 3 * 2
        y_pos = self.y_pos
        while amount_hearts > (self.hearts - max_hearts) / 2 * 2:
            if amount_hearts > 1:
                self.screen.blit(self.heart_life, (self.x_pos, y_pos))
            elif amount_hearts == 1:
                self.screen.blit(self.heart_half_life, (self.x_pos, y_pos))
            elif amount_hearts <= 0:
                self.screen.blit(self.heart_death, (self.x_pos, y_pos))
            amount_hearts -= 2
            y_pos += 40

