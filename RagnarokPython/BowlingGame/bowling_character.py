import os
import pygame

TRANSPARENT_COLOR = (250, 0, 250)


class bowling_character(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_type, player_type, velocity):
        super(bowling_character, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.player_type = player_type
        image = os.getcwd() + "\\Images\\BowlingGame\\%s" % self.player_type + \
                              "\\character_mode%s" % str(image_type) + ".png"
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(TRANSPARENT_COLOR)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.velocity = velocity

    def update_position(self, type_move):
        if type_move == 0 and self.x_pos < 270:  # move to the right
            self.x_pos += self.velocity
        elif type_move == 1 and self.x_pos > 205:  # move to the left
            self.x_pos -= self.velocity

    def update_image_type(self, image_type):
        image = os.getcwd() + "\\Images\\BowlingGame\\%s" % self.player_type + \
                              "\\character_mode%s" % str(image_type) + ".png"
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(TRANSPARENT_COLOR)

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))
