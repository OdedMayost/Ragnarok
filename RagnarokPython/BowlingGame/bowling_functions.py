from BowlingGame.bowling_pin import *


def bowling_background(screen):
    background_picture = pygame.image.load(os.getcwd() + "\\Images\\BowlingGame\\bowling_background.png")
    screen.blit(background_picture, (0, 0))


def pins():
    pins_list = pygame.sprite.Group()
    for pin_pos in range(10):
        if pin_pos < 4:
            pin = bowling_pin(220 + pin_pos * 30, 35)
        elif pin_pos < 7:
            pin = bowling_pin(235 + (pin_pos - 4) * 30, 65)
        elif pin_pos < 9:
            pin = bowling_pin(250 + (pin_pos - 7) * 30, 95)
        elif pin_pos < 10:
            pin = bowling_pin(265, 125)
        pins_list.add(pin)
    return pins_list
