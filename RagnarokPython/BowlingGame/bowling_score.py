import os
import pygame


class bowling_score(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super(bowling_score, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.player_score = [None, None, None, None, None, None, None, None, None, None]
        self.enemy_score = [None, None, None, None, None, None, None, None, None, None]
        self.round_number = 0
        self.font = pygame.font.Font(os.getcwd() + "\\Fonts\\BasicLight.ttf", 17)

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.x_pos, self.y_pos), (self.x_pos + self.width, self.y_pos), 2)

        pygame.draw.line(screen, (0, 0, 0), (self.x_pos, self.y_pos), (self.x_pos, self.y_pos + self.height), 2)

        pygame.draw.line(screen, (0, 0, 0), (self.x_pos, self.y_pos + self.height),
                         (self.x_pos + self.width, self.y_pos + self.height), 2)

        pygame.draw.line(screen, (0, 0, 0), (self.x_pos + self.width - 2, self.y_pos),
                         (self.x_pos + self.width - 2, self.y_pos + self.height), 2)

        pygame.draw.line(screen, (0, 0, 0), (self.x_pos + self.width - 40, self.y_pos),
                         (self.x_pos + self.width - 40, self.y_pos + self.height), 3)

        pygame.draw.line(screen, (0, 0, 0), (self.x_pos + self.width - 100, self.y_pos),
                         (self.x_pos + self.width - 100, self.y_pos + self.height), 2)

        pygame.draw.line(screen, (0, 0, 0), (self.x_pos, self.y_pos + 75),
                         (self.x_pos + self.width, self.y_pos + 75), 3)

        for position in range(11):
            pygame.draw.line(screen, (0, 0, 0), (self.x_pos, self.y_pos + 75 + 55 * position),
                             (self.x_pos + self.width, self.y_pos + 75 + 55 * position), 2)

        player = self.font.render("Player", True, (0, 0, 0))
        screen.blit(player, (547, 25))

        enemy = self.font.render("Enemy", True, (0, 0, 0))
        screen.blit(enemy, (607, 25))

        for position in range(10):
            number = self.font.render("%s" % str(position + 1), True, (0, 0, 0))
            screen.blit(number, (675, 100 + 55 * position))

        for position in range(10):
            if self.player_score[position] is not None:
                player_score = self.font.render("%s" % str(self.player_score[position]), True, (0, 0, 0))
                screen.blit(player_score, (565, 100 + 55 * position))
        player_score = 0
        for position in range(10):
            if self.player_score[position] is not None:
                player_score += self.player_score[position]
        player_score = self.font.render("%s" % str(player_score), True, (0, 0, 0))
        screen.blit(player_score, (565, 650))

        for position in range(10):
            if self.enemy_score[position] is not None:
                enemy_score = self.font.render("%s" % str(self.enemy_score[position]), True, (0, 0, 0))
                screen.blit(enemy_score, (625, 100 + 55 * position))
        enemy_score = 0
        for position in range(10):
            if self.enemy_score[position] is not None:
                enemy_score += self.enemy_score[position]
        enemy_score = self.font.render("%s" % str(enemy_score), True, (0, 0, 0))
        screen.blit(enemy_score, (625, 650))

    def update_score(self, player_type, score):
        if player_type == 0:
            if self.player_score[self.round_number] is None:
                self.player_score[self.round_number] = score
            else:
                self.player_score[self.round_number] += score
        elif player_type == 1:
            if self.enemy_score[self.round_number] is None:
                self.enemy_score[self.round_number] = score
            else:
                self.enemy_score[self.round_number] += score

    def update_round_number(self):
        self.round_number += 1
