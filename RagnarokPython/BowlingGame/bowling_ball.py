import os
import math
import pygame

TRANSPARENT_COLOR = (250, 0, 250)


class bowling_ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_type, player_type):
        super(bowling_ball, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.player_type = player_type
        self.image_type = image_type
        image = os.getcwd() + "\\Images\\BowlingGame\\%s" % self.player_type + \
                              "\\bowling_ball_mode%s" % str(self.image_type) + ".png"
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey(TRANSPARENT_COLOR)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.velocity = None
        self.throw_angle = None
        self.position = None

    def throwing_bowling_ball(self, acceleration, throw_angle):
        self.velocity = acceleration / 2
        if throw_angle < 30:
            self.throw_angle = throw_angle + 30
        elif throw_angle > 150:
            self.throw_angle = throw_angle - 30
        else:
            self.throw_angle = throw_angle
        self.position = 0
        self.image_type = 1

    def update_position(self):
        if self.x_pos >= 305:  # move to the right
            self.throw_angle = 180 - self.throw_angle
        elif self.x_pos <= 200:  # move to the left
            self.throw_angle = 180 - self.throw_angle

        if self.position == 3:
            if self.image_type == 3:
                self.image_type = 1
            else:
                self.image_type += 1
            self.position = 0
        self.position += 1
        image = os.getcwd() + "\\Images\\BowlingGame\\%s" % self.player_type + \
                              "\\bowling_ball_mode%s" % str(self.image_type) + ".png"
        self.image = pygame.image.load(image)
        self.image.set_colorkey(TRANSPARENT_COLOR)

        self.x_pos += self.velocity * math.cos(self.throw_angle / 180 * math.pi)
        self.y_pos -= self.velocity * math.sin(self.throw_angle / 180 * math.pi)
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def ball_position(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def update_x_pos(self, update_type, amount):
        if update_type == 0 and self.x_pos < 300:  # move to the right
            self.x_pos += amount
            self.rect.x = self.x_pos
        elif update_type == 1 and self.x_pos > 225:  # move to the left
            self.x_pos -= amount
            self.rect.x = self.x_pos

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))
