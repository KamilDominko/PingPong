import pygame as pg
import sys, random

RED = (255, 000, 000)
GREEN = (000, 255, 000)
BLUE = (000, 000, 255)
BLACK = (000, 000, 000)
WHITE = (255, 255, 255)


class Player:
    def __init__(self, game):
        self.width = 10
        self.height = 140
        self.rect = pg.Rect(game.screen_width - 20, game.screen_height / 2 - 15,
                            self.width, self.height)
        self.speed = 0
        self.acceleration = 7
        self.score = 0

    def player_movement(self, game):
        self.rect.y += self.speed
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= game.screen_height:
            self.rect.bottom = game.screen_height

    def draw(self, game):
        pg.draw.rect(game.screen, WHITE, self.rect)


class Oponent:
    def __init__(self, game):
        self.width = 10
        self.height = 140
        self.rect = pg.Rect(10, game.screen_height / 2 - 70, 10, 140)
        self.speed = 0
        self.acceleration = 7
        self.score = 0

    def oponent_movement(self, game):
        if self.rect.top < game.ball.rect.y:
            self.rect.top += self.acceleration
        if self.rect.bottom > game.ball.rect.y:
            self.rect.bottom -= self.acceleration
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= game.screen_height:
            self.rect.bottom = game.screen_height

    def draw(self, game):
        pg.draw.rect(game.screen, WHITE, self.rect)


class Ball:
    def __init__(self, game):
        self.width = 30
        self.height = 30
        self.rect = pg.Rect(game.screen_width / 2, game.screen_height / 2,
                            self.width, self.height)
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))

    def reset(self, game):
        current_time = pg.time.get_ticks()
        self.rect.center = (game.screen_width / 2, game.screen_height / 2)
        if current_time - game.score_time < 1000:
            no_3 = game.game_font.render("3", True, WHITE)
            game.screen.blit(no_3, (game.screen_width / 2 - 10, game.screen_height / 2 + 20))
        if 1000 < current_time - game.score_time < 2000:
            no_2 = game.game_font.render("2", True, WHITE)
            game.screen.blit(no_2, (game.screen_width / 2 - 10, game.screen_height / 2 + 20))
        if 2000 < current_time - game.score_time < 3000:
            no_1 = game.game_font.render("1", True, WHITE)
            game.screen.blit(no_1, (game.screen_width / 2 - 10, game.screen_height / 2 + 20))

        if current_time - game.score_time < 3000:
            self.speed_x, self.speed_y = 0, 0
        else:
            self.speed_x = 7 * random.choice((1, -1))
            self.speed_y = 7 * random.choice((1, -1))
            game.score_time = None

    def ball_movement(self, game):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= game.screen_height:
            self.speed_y *= -1
        if self.rect.left <= 0:
            game.player.score += 1
            game.score_time = pg.time.get_ticks()
        if self.rect.right >= game.screen_width:
            game.oponent.score += 1
            game.score_time = pg.time.get_ticks()
        if self.rect.colliderect(game.player.rect) or self.rect.colliderect(game.oponent.rect):
            self.speed_x *= -1

    def draw(self, game):
        pg.draw.ellipse(game.screen, WHITE, self.rect)


class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.FPS = 59
        self.screen_width = 1280
        self.screen_height = 960
        self.running = False
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Ping-Pong")
        self.game_font = None
        self.score_time = 1

        self.player = Player(self)
        self.oponent = Oponent(self)
        self.ball = Ball(self)

    def main_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.player.speed += self.player.acceleration
                if event.key == pg.K_UP:
                    self.player.speed -= self.player.acceleration
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    self.player.speed -= self.player.acceleration
                if event.key == pg.K_UP:
                    self.player.speed += self.player.acceleration

    def draw_stats(self):
        player_text = self.game_font.render(f"{self.player.score}", True, WHITE)
        self.screen.blit(player_text, (660, 470))
        oponent_text = self.game_font.render(f"{self.oponent.score}", True, WHITE)
        self.screen.blit(oponent_text, (600, 470))

    def sprites_movement(self):
        self.player.player_movement(self)
        self.oponent.oponent_movement(self)
        self.ball.ball_movement(self)

    def draw_sprites(self):
        self.player.draw(self)
        self.oponent.draw(self)
        self.ball.draw(self)

    def start(self):
        pg.init()
        self.game_font = pg.font.Font("freesansbold.ttf", 32)
        self.running = True
        while self.running:
            self.main_loop()

            self.sprites_movement()

            self.screen.fill(BLACK)
            pg.draw.aaline(self.screen, WHITE, (self.screen_width // 2, 0),
                           (self.screen_width // 2, self.screen_height))

            self.draw_sprites()

            if self.score_time:
                self.ball.reset(self)

            self.draw_stats()

            pg.display.flip()
            self.clock.tick(self.FPS)


gra = Game()
gra.start()
