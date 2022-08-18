import pygame as pg
import sys, random


def ball_animation():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_reset()

    if ball.colliderect(player) or ball.colliderect(oponent):
        ball_speed_x *= -1

def ball_reset():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width//2, screen_height//2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def oponent_animation():
    if oponent.top < ball.y:
        oponent.top += oponent_speed
    if oponent.bottom > ball.y:
        oponent.bottom -= oponent_speed
    if oponent.top <= 0:
       oponent.top = 0
    if oponent.bottom >= screen_height:
       oponent.bottom = screen_height

# General setup
pg.init()
clock = pg.time.Clock()

# Setting up the main window
FPS = 59
screen_width = 1280
screen_height = 960
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Pong")

# Game rectangles
ball = pg.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pg.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
oponent = pg.Rect(10, screen_height / 2 - 70, 10, 140)

ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
oponent_speed = 7

bg_color = pg.Color("grey12")
light_grey = (200, 200, 200)

while True:
    # Handling input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                player_speed += 7
            if event.key == pg.K_UP:
                player_speed -= 7
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                player_speed -= 7
            if event.key == pg.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    oponent_animation()

    # Visuals
    screen.fill(bg_color)
    pg.draw.rect(screen, light_grey, player)
    pg.draw.rect(screen, light_grey, oponent)
    pg.draw.ellipse(screen, light_grey, ball)
    pg.draw.aaline(screen, light_grey, (screen_width // 2, 0), (screen_width // 2, screen_height))

    # Updating the window
    pg.display.flip()
    clock.tick(FPS)
