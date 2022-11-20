from tcp_by_size import send_by_size, receive_by_size
import threading
import socket
import random
import time
import os

import moviepy.editor
import pygame

from BowlingGame.bowling_character import *
from BowlingGame.bowling_functions import *
from BowlingGame.bowling_score import *
from BowlingGame.bowling_ball import *
from BowlingGame.bowling_pin import *

from RockHero.Arrow import *
from RockHero.Life import *

# ----------------------------------------------------------------------------------------------------


ip = "0.0.0.0"

port_android_client = 50000

ip_super_server = "172.20.10.6"
port_super_server = 55555

threads = []
threads_mode = True

android_message = []
android_message_lock = threading.Lock()
android_thread_mode = True
android_thread_mode_lock = threading.Lock()

super_server_message = []
super_server_message_lock = threading.Lock()
super_server_thread_mode = True
super_server_thread_mode_lock = threading.Lock()

game_message = []
game_message_lock = threading.Lock()
type_game = None
game_mode = True

arrow_mode = True
player_arrows = pygame.sprite.Group()
enemy_arrows = pygame.sprite.Group()
explosion = [[], []]
create_arrow = []

FPS = 50
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 775


# ----------------------------------------------------------------------------------------------------


def android_client_service(android_client_socket):
    global super_server_message
    global super_server_message_lock
    global android_thread_mode
    global android_thread_mode_lock
    global game_message
    global game_message_lock
    global threads_mode

    android_thread_mode_lock.acquire()
    android_thread_mode = True
    android_thread_mode_lock.release()
    android_thread = threading.Thread(target=handle_android_messages, args=(android_client_socket,))
    android_thread.start()

    while threads_mode:
        data = receive_by_size(android_client_socket).decode("utf8")
        if data == "":
            android_thread_mode_lock.acquire()
            android_thread_mode = False
            android_thread_mode_lock.release()
            android_thread.join()
            print("Android client disconnected")
            break

        print("Received from Android client --> " + str(data))
        data = data.split("~")

        if data[0] == "SGNUP":
            message = "~".join(data)
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()

        elif data[0] == "SGNIN":
            message = "~".join(data)
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()

        elif data[0] == "MOVES":
            message = "~".join(data)
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        elif data[0] == "CHOSE":
            message = "~".join(data)
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        elif data[0] == "PMOVE":
            message = "~".join(data)
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        elif data[0] == "ACLRT":
            acceleration = str(round(float(data[1])))
            throw_angle = str(round(float(data[2])))
            message = data[0] + "~" + acceleration + "~" + throw_angle
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        elif data[0] == "PRESS":
            message = "~".join(data)
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

    android_thread_mode_lock.acquire()
    android_thread_mode = False
    android_thread_mode_lock.release()
    android_thread.join()
    print("Communication with the Android client was disconnected")
    android_client_socket.close()


def handle_android_messages(client_socket):
    global android_thread_mode
    global android_message
    global android_message_lock

    while android_thread_mode:
        if len(android_message) != 0:
            android_message_lock.acquire()
            message = android_message.pop(0)
            android_message_lock.release()
            send_by_size(client_socket, message.encode())
            print("Sent to Android client --> " + str(message))


# ----------------------------------------------------------------------------------------------------


def super_server_service(server_socket):
    global type_game
    global threads_mode
    global game_message
    global game_message_lock
    global android_message
    global android_message_lock
    global super_server_thread_mode
    global super_server_thread_mode_lock

    super_server_thread_mode_lock.acquire()
    super_server_thread_mode = True
    super_server_thread_mode_lock.release()
    super_server_thread = threading.Thread(target=handle_super_server_messages, args=(server_socket,))
    super_server_thread.start()

    while threads_mode:
        data = receive_by_size(server_socket).decode("utf8")
        if data == "":
            super_server_thread_mode_lock.acquire()
            super_server_thread_mode = False
            super_server_thread_mode_lock.release()
            super_server_thread.join()
            print("Super server disconnected")
            break

        print("Received from super server --> " + str(data))
        data = data.split("~")

        if data[0] == "REGIS":
            message = "~".join(data)
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        elif data[0] == "LOGIN":
            message = "~".join(data)
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        elif data[0] == "START":
            message = data[0] + "~" + data[1]
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()
            message = data[0] + "~" + data[2]
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()

        if type_game == "bowling game":
            if data[0] == "ENDED":
                message = "~".join(data)
                android_message_lock.acquire()
                android_message.append(message)
                android_message_lock.release()
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "RNDOV":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "ENPIN":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "ENMOV":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "ENACL":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

        elif type_game == "Rock Hero":
            if data[0] == "ENDED":
                message = "~".join(data)
                android_message_lock.acquire()
                android_message.append(message)
                android_message_lock.release()
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "GSONG":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "EMISS":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "ENKEY":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

            elif data[0] == "ARROW":
                message = "~".join(data)
                game_message_lock.acquire()
                game_message.append(message)
                game_message_lock.release()

    super_server_thread_mode_lock.acquire()
    super_server_thread_mode = False
    super_server_thread_mode_lock.release()
    super_server_thread.join()
    print("Communication with the Super server was disconnected")
    server_socket.close()


def handle_super_server_messages(server_socket):
    global super_server_thread_mode
    global super_server_message
    global super_server_message_lock

    while super_server_thread_mode:
        if len(super_server_message) != 0:
            super_server_message_lock.acquire()
            message = super_server_message.pop(0)
            super_server_message_lock.release()
            send_by_size(server_socket, message.encode())
            print("Sent to super sever --> " + str(message))


# ----------------------------------------------------------------------------------------------------


def bowling_game(screen, clock, first_player):
    global game_mode
    global super_server_message
    global super_server_message_lock

    scoreboard = bowling_score(540, 0, 160, 680)

    if first_player == "1":
        while game_mode:

            scoreboard = bowling_player_turn(screen, clock, scoreboard)

            if game_mode:
                scoreboard = bowling_enemy_turn(screen, clock, scoreboard)

            scoreboard.update_round_number()
            if scoreboard.round_number == 10:
                if scoreboard.player_score < scoreboard.enemy_score:
                    message = "ENDED"
                    super_server_message_lock.acquire()
                    super_server_message.append(message)
                    super_server_message_lock.release()
                    game_mode = False
                    android_message_lock.acquire()
                    android_message.append(message)
                    android_message_lock.release()

        if scoreboard.player_score > scoreboard.enemy_score:
            bowling_winning_screen(screen, clock)
        elif scoreboard.player_score == scoreboard.enemy_score:
            bowling_draw_screen(screen, clock)
        elif scoreboard.player_score < scoreboard.enemy_score:
            bowling_losing_game(screen, clock)

    elif first_player == "2":
        while game_mode:
            scoreboard = bowling_enemy_turn(screen, clock, scoreboard)
            if game_mode:
                scoreboard = bowling_player_turn(screen, clock, scoreboard)

            scoreboard.update_round_number()
            if scoreboard.round_number == 10:
                if scoreboard.player_score < scoreboard.enemy_score:
                    message = "ENDED"
                    super_server_message_lock.acquire()
                    super_server_message.append(message)
                    super_server_message_lock.release()
                    game_mode = False
                    android_message_lock.acquire()
                    android_message.append(message)
                    android_message_lock.release()

        if scoreboard.player_score > scoreboard.enemy_score:
            bowling_winning_screen(screen, clock)
        elif scoreboard.player_score == scoreboard.enemy_score:
            bowling_draw_screen(screen, clock)
        elif scoreboard.player_score < scoreboard.enemy_score:
            bowling_losing_game(screen, clock)


def bowling_player_turn(screen, clock, scoreboard):
    global game_mode
    global threads_mode
    global game_message
    global game_message_lock
    global android_message
    global android_message_lock
    global super_server_message
    global super_server_message_lock

    player = bowling_character(240, 540, 1, "player", 3)
    player_ball = bowling_ball(252, 540, 1, "player")

    enemy = bowling_character(600, 700, 2, "enemy", 3)

    ball_loop = False
    pins_list = pins()

    score = 0

    round_number = 0
    finish = [False, False]
    turn_over = False
    while not turn_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                message = "ENDED"
                super_server_message_lock.acquire()
                super_server_message.append(message)
                super_server_message_lock.release()
                android_message_lock.acquire()
                android_message.append(message)
                android_message_lock.release()
                threads_mode = False
                exit()

        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = ""
        data = data.split("~")

        if data[0] == "PMOVE":
            if data[1] == "1":
                player.update_position(0)
                player_ball.update_x_pos(0, player.velocity)
            elif data[1] == "2":
                player.update_position(1)
                player_ball.update_x_pos(1, player.velocity)

        elif data[0] == "ACLRT":
            if not ball_loop:
                player_ball.throwing_bowling_ball(int(data[1]), int(data[2]))
                ball_loop = True
                player.update_image_type(2)

        elif data[0] == "RNDOV":
            finish[1] = True

        elif data[0] == "ENDED":
            game_mode = False
            turn_over = True
            message = "ENDED"
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()

        bowling_background(screen)

        scoreboard.draw(screen)

        list_fallen_pins = pygame.sprite.spritecollide(player_ball, pins_list, True)

        if ball_loop:
            if player_ball.y_pos > 35:
                player_ball.update_position()
                player_ball.draw(screen)
                if list_fallen_pins:
                    score += len(list_fallen_pins)
            else:
                ball_loop = False
                scoreboard.update_score(0, score)
                message = "PINUM~" + str(score)
                super_server_message_lock.acquire()
                super_server_message.append(message)
                super_server_message_lock.release()
                player.update_image_type(1)
                player_ball.ball_position(player.x_pos + 12, player.y_pos)
                round_number += 1
                score = 0
                if round_number == 2:
                    message = "RNDOV"
                    super_server_message_lock.acquire()
                    super_server_message.append(message)
                    super_server_message_lock.release()
                    finish[0] = True

        player.draw(screen)
        enemy.draw(screen)

        pins_list.draw(screen)

        if finish[0] and finish[1]:
            turn_over = True

        pygame.display.flip()
        clock.tick(FPS)

    return scoreboard


def bowling_enemy_turn(screen, clock, scoreboard):
    global game_mode
    global threads_mode
    global game_message
    global game_message_lock
    global android_message
    global android_message_lock
    global super_server_message
    global super_server_message_lock

    enemy = bowling_character(240, 540, 1, "enemy", 3)
    enemy_ball = bowling_ball(252, 540, 1, "enemy")

    player = bowling_character(600, 700, 2, "player", 3)

    ball_loop = False
    pins_list = pins()

    round_number = 0
    finish = [False, False]
    turn_over = False
    while not turn_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                message = "ENDED"
                super_server_message_lock.acquire()
                super_server_message.append(message)
                super_server_message_lock.release()
                android_message_lock.acquire()
                android_message.append(message)
                android_message_lock.release()
                threads_mode = False
                exit()

        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = ""
        data = data.split("~")

        if data[0] == "ENMOV":
            if data[1] == "1":
                enemy.update_position(0)
                enemy_ball.update_x_pos(0, enemy.velocity)
            elif data[1] == "2":
                enemy.update_position(1)
                enemy_ball.update_x_pos(1, enemy.velocity)

        elif data[0] == "ENACL":
            if not ball_loop:
                enemy_ball.throwing_bowling_ball(int(data[1]), int(data[2]))
                ball_loop = True
                enemy.update_image_type(2)

        elif data[0] == "ENPIN":
            scoreboard.update_score(1, int(data[1]))

        elif data[0] == "RNDOV":
            finish[0] = True

        elif data[0] == "ENDED":
            game_mode = False
            turn_over = True
            message = "ENDED"
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()

        bowling_background(screen)

        scoreboard.draw(screen)

        pygame.sprite.spritecollide(enemy_ball, pins_list, True)

        if ball_loop:
            if enemy_ball.y_pos > 35:
                enemy_ball.update_position()
                enemy_ball.draw(screen)
            else:
                ball_loop = False
                enemy.update_image_type(1)
                enemy_ball.ball_position(enemy.x_pos + 12, enemy.y_pos)
                round_number += 1
                if round_number == 2:
                    finish[1] = True
                    message = "RNDOV"
                    super_server_message_lock.acquire()
                    super_server_message.append(message)
                    super_server_message_lock.release()

        enemy.draw(screen)
        player.draw(screen)

        pins_list.draw(screen)

        if finish[0] and finish[1]:
            turn_over = True

        pygame.display.flip()
        clock.tick(FPS)

    return scoreboard


def bowling_winning_screen(screen, clock):
    font = pygame.font.Font(os.getcwd() + "\\Fonts\\Pixle_Font.ttf", 75)
    text = "you are the winner"
    red = 200
    green = 50
    blue = 75
    x_pos = (700 - (font.render(text, True, (red, green, blue))).get_size()[0]) / 2
    y_pos = 350

    screen_time = 1
    velocity_red = 20
    velocity_green = 5
    velocity_blue = 15

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

        if screen_time == 250:
            finish = True

        bowling_end_screen = pygame.image.load(os.getcwd() + "\\Images\\BowlingGame\\BowlingEndScreen.png")
        screen.blit(bowling_end_screen, (0, 0))

        if red < 20 or red > 235:
            velocity_red *= -1
        if green < 5 or green > 250:
            velocity_green *= -1
        if blue < 15 or blue > 240:
            velocity_blue *= -1

        if screen_time % 5 == 0:
            red += velocity_red
            green += velocity_green
            blue += velocity_blue

        print_text = font.render(text, True, (red, green, blue))
        screen.blit(print_text, (x_pos, y_pos))

        screen_time += 1

        pygame.display.flip()
        clock.tick(FPS)


def bowling_losing_game(screen, clock):
    font = pygame.font.Font(os.getcwd() + "\\Fonts\\Pixle_Font.ttf", 55)
    color = (150, 0, 200)
    y_pos = 360

    screen_time = 1
    position = 0

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

        if screen_time == 250:
            finish = True

        bowling_end_screen = pygame.image.load(os.getcwd() + "\\Images\\BowlingGame\\BowlingEndScreen.png")
        screen.blit(bowling_end_screen, (0, 0))

        if position == 0:
            text = "You have been defeated"
            print_text = font.render(text, True, color)
            x_pos = (700 - print_text.get_size()[0]) / 2

        elif position == 1:
            text = "You have been defeated."
            print_text = font.render(text, True, color)
            x_pos = (700 - print_text.get_size()[0]) / 2

        elif position == 2:
            text = "You have been defeated.."
            print_text = font.render(text, True, color)
            x_pos = (700 - print_text.get_size()[0]) / 2

        elif position == 3:
            text = "You have been defeated..."
            print_text = font.render(text, True, color)
            x_pos = (700 - print_text.get_size()[0]) / 2

        screen.blit(print_text, (x_pos, y_pos))

        screen_time += 1
        if screen_time % 25 == 0:
            if position == 4:
                position = 0
            else:
                position += 1

        pygame.display.flip()
        clock.tick(FPS)


def bowling_draw_screen(screen, clock):
    font = pygame.font.Font(os.getcwd() + "\\Fonts\\Pixle_Font.ttf", 75)
    text = "Its a tie"
    print_text = font.render(text, True, (0, 0, 255))
    x_pos = (700 - print_text.get_size()[0]) / 2
    y_pos = 350

    screen_time = 1

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

        if screen_time == 250:
            finish = True

        if screen_time % 5 == 0:
            bowling_end_screen = pygame.image.load(os.getcwd() + "\\Images\\BowlingGame\\BowlingEndScreen.png")
            screen.blit(bowling_end_screen, (0, 0))
        else:
            bowling_end_screen = pygame.image.load(os.getcwd() + "\\Images\\BowlingGame\\BowlingEndScreen.png")
            screen.blit(bowling_end_screen, (0, 0))
            screen.blit(print_text, (x_pos, y_pos))

        screen_time += 1

        pygame.display.flip()
        clock.tick(FPS)


# ----------------------------------------------------------------------------------------------------


def rock_hero(screen, clock, first_player):
    global game_mode
    global threads_mode
    global game_message
    global game_message_lock
    global android_message
    global android_message_lock
    global super_server_message
    global super_server_message_lock
    global player_arrows
    global enemy_arrows
    global create_arrow
    global explosion

    background = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\Background.png")

    player_life = Life(screen, 3, 3)
    enemy_life = Life(screen, 658, 3)

    if len(game_message) != 0:
        game_message_lock.acquire()
        data = game_message.pop(0)
        game_message_lock.release()
    else:
        data = "~"
    data = data.split("~")
    while data[0] != "GSONG":
        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = "~"
        data = data.split("~")
    game_music(int(data[1]))

    if first_player == "1":
        time_now = round(time.time() * 1000)
        create_arrow_thread = threading.Thread(target=create_arrows, args=(time_now,))
        create_arrow_thread.start()

    winner = 0
    arrow_creation_time = 0
    count_player_explosions = 0
    count_enemy_explosions = 0
    key_type = ["Right", "Left", "Up", "Down"]

    while game_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                message = "ENDED"
                super_server_message_lock.acquire()
                super_server_message.append(message)
                super_server_message_lock.release()
                android_message_lock.acquire()
                android_message.append(message)
                android_message_lock.release()
                threads_mode = False
                exit()

        screen.blit(background, (0, 0))

        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = ""
        data = data.split("~")

        if data[0] == "PRESS":
            key = key_type[int(data[1])]
            is_explode = False
            for arrow in player_arrows.sprites():
                if 680 <= arrow.y_pos <= 760:
                    if key == key_type[arrow.arrow_type]:
                        explosion[0] = [arrow.image_explode, (arrow.x_pos, 699)]
                        arrow.kill()
                        is_explode = True
                        message = "PRESS~1"
                        super_server_message_lock.acquire()
                        super_server_message.append(message)
                        super_server_message_lock.release()
            if not is_explode:
                message = "PRESS~2"
                super_server_message_lock.acquire()
                super_server_message.append(message)
                super_server_message_lock.release()
                player_life.remove_life("HeartHalfLife")

        elif data[0] == "ENKEY":
            if data[1] == "1":
                for arrow in enemy_arrows.sprites():
                    if 680 <= arrow.y_pos:
                        explosion[1] = [arrow.image_explode, (arrow.xpos, 699)]
                        arrow.kill()
            elif data[1] == "2":
                enemy_life.remove_life("HeartHalfLife")

        elif data[0] == "EMISS":
            miss_arrow(enemy_arrows, enemy_life)

        elif data[0] == "ARROW":
            create_arrow.append(data[1])

        elif data[0] == "ENDED":
            game_mode = False
            winner = 1
            message = "ENDED"
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()

        if player_life.hearts == 0:
            game_mode = False
            winner = 2
            message = "ENDED"
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()
            android_message_lock.acquire()
            android_message.append(message)
            android_message_lock.release()

        miss_arrow(player_arrows, player_life)

        if arrow_creation_time == 30:
            if len(create_arrow) != 0:
                type_arrow = create_arrow.pop(0)
                arrow = Arrow(type_arrow, 5, screen, 28, "Player")
                player_arrows.add(arrow)
                arrow = Arrow(type_arrow, 5, screen, 378, "Enemy")
                enemy_arrows.add(arrow)
            arrow_creation_time = 0
        else:
            arrow_creation_time += 1

        player_arrows.update()
        enemy_arrows.update()

        if count_player_explosions == 20:
            explosion[0] = []
            count_player_explosions = 0
        elif explosion:
            if len(explosion[0]) != 0:
                screen.blit(explosion[0][0], explosion[0][1])
                count_player_explosions += 1

        if count_enemy_explosions == 20:
            explosion[1] = []
            count_enemy_explosions = 0
        elif explosion:
            if len(explosion[1]) != 0:
                screen.blit(explosion[1][0], explosion[1][1])
                count_enemy_explosions += 1

        player_life.print_life()
        enemy_life.print_life()

        pygame.display.flip()
        clock.tick(FPS)

    if winner == 1:
        victory = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\EndScreens\\VictoryScreen.png")
        screen.blit(victory, (0, 0))
        pygame.mixer.music.stop()
        pygame.display.flip()
    elif winner == 2:
        defeat = pygame.image.load(os.getcwd() + "\\Images\\RockHero\\EndScreens\\DefeatScreen.png")
        screen.blit(defeat, (0, 0))
        pygame.mixer.music.stop()
        pygame.display.flip()

    if first_player == "1":
        create_arrow_thread.join()

    time.sleep(2.5)


def game_music(type_music):
    music = [os.getcwd() + "\\Music\\Alice Cooper - School's Out.mp3",
             os.getcwd() + "\\Music\\Poison - Talk Dirty To Me.mp3",
             os.getcwd() + "\\Music\\The Strokes - Reptilia.mp3",
             os.getcwd() + "\\Music\\Priestess - Lay Down.mp3",
             os.getcwd() + "\\Music\\The Who - The Seeker.mp3"]
    pygame.mixer.init()
    pygame.mixer.music.load(music[type_music])
    pygame.mixer.music.play()


def create_arrows(time_arrow):
    global game_mode
    global arrow_mode
    global game_message
    global game_message_lock
    global super_server_message
    global super_server_message_lock

    while game_mode and arrow_mode:
        time_now = round(time.time() * 1000)
        if (time_now - time_arrow) >= 600:
            type_arrow = random.randint(0, 3)
            message = "ARROW~" + str(type_arrow)
            super_server_message_lock.acquire()
            super_server_message.append(message)
            super_server_message_lock.release()
            game_message_lock.acquire()
            game_message.append(message)
            game_message_lock.release()
            time_arrow = time_now


def miss_arrow(arrows, life):
    global player_arrows
    global super_server_message
    global super_server_message_lock

    for arrow in arrows.sprites():
        if arrow.y_pos > 775:
            arrow.kill()
            life.remove_life("HeartDeath")
            if arrows == player_arrows:
                message = "MISSA"
                super_server_message_lock.acquire()
                super_server_message.append(message)
                super_server_message_lock.release()


# ----------------------------------------------------------------------------------------------------


def game_manager(screen, clock, font):
    global game_message_lock
    global game_message
    global threads_mode
    global type_game

    while threads_mode:
        homepage_screen(screen, clock, font)
        first_player = waiting_screen(screen, clock)
        if type_game == "bowling game":
            bowling_game(screen, clock, first_player)
        elif type_game == "Rock Hero":
            rock_hero(screen, clock, first_player)

    pygame.quit()
    threads_mode = False


def intro():
    pygame.init()
    video = moviepy.editor.VideoFileClip(".\\Videos\\Intro.mpeg")
    video.preview()


def opening_screen(screen, computer_id):
    computer_id_background = pygame.image.load(os.getcwd() + "\\Images\\ComputerID.png")
    screen.blit(computer_id_background, (0, 0))
    font = pygame.font.Font(os.getcwd() + "\\Fonts\\Pixle_Font.ttf", 50)
    computer_id = font.render(computer_id, True, (255, 255, 255))
    x_pos = 192 + ((308 - computer_id.get_size()[0]) / 2)
    screen.blit(computer_id, (x_pos, 400))
    pygame.display.flip()


def homepage_screen(screen, clock, font):
    global game_message_lock
    global game_message
    global threads_mode
    global type_game

    game_selection = "bowling game"
    if len(game_message) != 0:
        game_message_lock.acquire()
        data = game_message.pop(0)
        game_message_lock.release()
    else:
        data = ""
    data = data.split("~")

    while data[0] != "CHOSE":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                threads_mode = False
                exit()

        homepage = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\Homepage.png")
        screen.blit(homepage, (0, 0))

        if game_selection == "bowling game":
            text_box = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\text_frame.png")
            screen.blit(text_box, (100, 250))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 250, 500, 75), 3)

            bowling = font.render("Bowling Game", True, (255, 255, 255))
            x_pos = 100 + ((500 - bowling.get_size()[0]) / 2)
            screen.blit(bowling, (x_pos, 265))

            bowling = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\BowlingGame.png")
            screen.blit(bowling, (100, 450))

            text_box = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\text_frame.png")
            screen.blit(text_box, (100, 350))
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(100, 350, 500, 75), 3)

            rock_hero_font = font.render("Rock Hero", True, (255, 255, 255))
            x_pos = 100 + ((500 - rock_hero_font.get_size()[0]) / 2)
            screen.blit(rock_hero_font, (x_pos, 365))

        elif game_selection == "Rock Hero":
            text_box = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\text_frame.png")
            screen.blit(text_box, (100, 250))
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(100, 250, 500, 75), 3)

            bowling = font.render("Bowling Game", True, (255, 255, 255))
            x_pos = 100 + ((500 - bowling.get_size()[0]) / 2)
            screen.blit(bowling, (x_pos, 265))

            text_box = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\text_frame.png")
            screen.blit(text_box, (100, 350))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 350, 500, 75), 3)

            rock_hero_font = font.render("Rock Hero", True, (255, 255, 255))
            x_pos = 100 + ((500 - rock_hero_font.get_size()[0]) / 2)
            screen.blit(rock_hero_font, (x_pos, 365))

            rock_hero_image = pygame.image.load(os.getcwd() + "\\Images\\Homepage\\RockHero.png")
            screen.blit(rock_hero_image, (100, 450))

        if data[0] == "MOVES":
            if game_selection == "bowling game":
                game_selection = "Rock Hero"
            elif game_selection == "Rock Hero":
                game_selection = "bowling game"

        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = ""
        data = data.split("~")

        pygame.display.flip()
        clock.tick(FPS)

    type_game = game_selection


def waiting_screen(screen, clock):
    global game_message_lock
    global game_message
    global threads_mode
    global type_game

    if type_game == "bowling game":
        message = "TYGAM~1"
    elif type_game == "Rock Hero":
        message = "TYGAM~2"
    super_server_message_lock.acquire()
    super_server_message.append(message)
    super_server_message_lock.release()

    if len(game_message) != 0:
        game_message_lock.acquire()
        data = game_message.pop(0)
        game_message_lock.release()
    else:
        data = ""
    data = data.split("~")

    position = 1
    screen_time = 1

    while data[0] != "START":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                threads_mode = False
                exit()

        standby_screen = pygame.image.load(os.getcwd() + "\\Images\\StandbyScreen\\"
                                                         "StandbyScreen%s" % str(position) + ".png")
        screen.blit(standby_screen, (0, 0))

        if screen_time % 10 == 0:
            if position == 4:
                position = 1
            else:
                position += 1

        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = ""
        data = data.split("~")

        screen_time += 1

        pygame.display.flip()
        clock.tick(FPS)

    first_player = data[1]
    return first_player


# ----------------------------------------------------------------------------------------------------


def main():
    global ip
    global ip_super_server
    global port_super_server
    global port_android_client
    global threads
    global game_message
    global game_message_lock

    server_socket = socket.socket()
    server_socket.connect((ip_super_server, port_super_server))
    message = "HELLO"
    send_by_size(server_socket, message.encode())
    data = (receive_by_size(server_socket).decode("utf8")).split("~")
    while data[0] != "COMID":
        data = (receive_by_size(server_socket).decode("utf8")).split("~")
    computer_id = data[1]
    data = "~".join(data)
    print("Received from super server --> " + str(data))

    intro()

    pygame.init()
    clock = pygame.time.Clock()
    screen_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(screen_size)
    icon = os.getcwd() + "\\Images\\Icon.png"
    icon = pygame.image.load(icon).convert()
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Ragnarok")
    font = pygame.font.Font(os.getcwd() + "\\Fonts\\Pixle_Font.ttf", 50)

    opening_screen(screen, computer_id)

    thread = threading.Thread(target=super_server_service, args=(server_socket,))
    thread.start()
    threads.append(thread)

    server_socket = socket.socket()
    server_socket.bind((ip, port_android_client))
    server_socket.listen(1)
    (android_client_socket, android_client_address) = server_socket.accept()
    thread = threading.Thread(target=android_client_service, args=(android_client_socket,))
    thread.start()
    threads.append(thread)

    if len(game_message) != 0:
        game_message_lock.acquire()
        data = game_message.pop(0)
        game_message_lock.release()
    else:
        data = "~"
    data = data.split("~")
    while (data[0] != "REGIS" and data[1] != "1") or (data[0] != "LOGIN" and data[1] != "1"):
        opening_screen(screen, computer_id)
        if len(game_message) != 0:
            game_message_lock.acquire()
            data = game_message.pop(0)
            game_message_lock.release()
        else:
            data = "~"
        data = data.split("~")

    thread = threading.Thread(target=game_manager, args=(screen, clock, font))
    thread.start()
    threads.append(thread)

    for process in threads:
        process.join()
    server_socket.close()


if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------------------------
