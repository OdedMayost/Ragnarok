import pygame
import os

TRANSPARENT_COLOR = (250, 0, 250)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, arrow_type, velocity, screen, position, type_explosion):
        pygame.sprite.Sprite.__init__(self)
        types = ["Right", "Left", "Up", "Down"]
        self.arrow_type = int(arrow_type)
        self.x_pos = position + self.arrow_type * 74
        self.y_pos = -72
        self.image = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\Arrows"
                                                     "\\%s" % types[self.arrow_type] + "Arrow.png")
        self.image.set_colorkey(TRANSPARENT_COLOR)
        self.image_explode = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\Arrows\\%s" % types[self.arrow_type] +
                                               type_explosion + "Explosion.png")
        self.velocity = velocity
        self.screen = screen

    def update(self):
        self.y_pos += self.velocity
        self.screen.blit(self.image, (self.x_pos, self.y_pos))

