import os
import pygame

TRANSPARENT_COLOR = (250, 0, 250)


class bowling_pin(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(bowling_pin, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.getcwd() + "\\Images\\BowlingGame\\pin.png").convert()
        self.image.set_colorkey(TRANSPARENT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def get_position(self):
        return self.rect.x, self.rect.y
