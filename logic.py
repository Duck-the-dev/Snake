import random
import sys
import pygame
from pygame.math import Vector2

pygame.init()


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 110, 125), snake_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy


class Fruit:
    def __init__(self):
        self.randomizer()

    def randomizer(self):
        self.y = random.randint(0, cell_num - 1)
        self.x = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (109, 147, 97), fruit_rect)


cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
box = pygame.Surface((500, 500))

ScreenUpdate = pygame.USEREVENT
pygame.time.set_timer(ScreenUpdate, 150)

game_font = pygame.font.Font(None, 35)

lost = False


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def again(self):
        # initiate all objects to their original values
        global lost
        lost = False
        self.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.snake.direction = Vector2(1, 0)
        self.snake.new_block = False

    def update(self):
        if not lost:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        if not lost:
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
        if lost:
            self.game_over()

    def check_collision(self):
        # what make you win
        if self.fruit.pos == self.snake.body[0]:
            self.snake.new_block = True
            self.fruit.randomizer()

    def check_fail(self):
        # what makes you lose
        global lost
        if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
            lost = True
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                lost = True

    def game_over(self):
        # Game Over screen

        text = "GameOver"
        back = pygame.Surface((int(cell_size * cell_num), int(cell_size * cell_num)))
        back.fill(pygame.Color("white"))
        game_over_surface = game_font.render(text, pygame.Color("black"), True)
        game_over_x = int(cell_size * cell_num / 2)
        game_over_y = int(cell_size * cell_num / 2)
        game_over_rect = game_over_surface.get_rect(center=(game_over_x, game_over_y))

        back_rect = back.get_rect(center=(game_over_x, game_over_y))
        screen.blit(back, back_rect)

        newline_sur = game_font.render("hit the \"Space bar\" to play again or \" Esc\" to Quit",
                                       pygame.Color("black"),
                                       True)

        newline_x = int(cell_size * cell_num / 2)
        newline_y = int(cell_size * cell_num / 2 + 50)
        newline_rect = newline_sur.get_rect(center=(newline_x, newline_y))
        screen.blit(newline_sur, newline_rect)

        screen.blit(game_over_surface, game_over_rect)
        score = "Your score is  : " + str(len(self.snake.body) - 3)
        back = pygame.Surface((120, 30))
        back.fill(pygame.Color("white"))

        score_sur = game_font.render(score, pygame.Color("black"), True)
        score_x = int(cell_size * cell_num / 2)
        score_y = int(cell_size * cell_num / 2 - 60)

        score_rect = score_sur.get_rect(center=(score_x, score_y))

        screen.blit(score_sur, score_rect)

    def draw_score(self):
        # Score box with white background
        score = "Score : " + str(len(self.snake.body) - 3)
        back = pygame.Surface((120, 30))
        back.fill(pygame.Color("white"))

        score_sur = game_font.render(score, pygame.Color("black"), True)
        score_x = int(cell_size * cell_num / 10)
        score_y = int(cell_size * cell_num / 10 - 60)
        back_rect = back.get_rect(center=(score_x, score_y))
        screen.blit(back, back_rect)

        score_rect = score_sur.get_rect(center=(score_x, score_y))
        screen.blit(score_sur, score_rect)


# game instance
main_game = Main()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ScreenUpdate:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main_game.again()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    screen.fill((174, 215, 69))
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)
