import pygame
import sys
from random import randint, uniform
import random
from collections import Counter


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


class Civilisation:
    def __init__(self, name):
        self.id = name
        self.color = game.color[name]
        self.power = game.power[name]


def get_neighbours(y, x):
    ans = []
    for i in range(max(0, y - 1), min(y + 2, map_height)):
        for j in range(max(0, x - 1), min(x + 2, map_width)):
            if not (i == y and j == x):
                ans.append([i, j])
    return ans


class Map:
    def __init__(self):
        self.map = [[Civilisation(0) for i in range(map_width)] for j in range(map_height)]
        self.x_text = map_width * square_size
        self.y_text = 0
        for c in game.civilisations:
            self.map[randint(0, map_height - 1)][randint(0, map_width - 1)] = Civilisation(c)

    def make_turn(self, name):
        new_map = self.map
        for y in range(map_height):
            for x in range(map_width):
                if self.map[y][x].id == name:
                    attacking = self.map[y][x]
                    neighbours = get_neighbours(y, x)
                    for y_n, x_n in neighbours:
                        if random.random() < attacking.power:
                            new_map[y_n][x_n] = Civilisation(attacking.id)
        self.map = new_map

    def check_end(self):
        return len(set([item.id for sublist in self.map for item in sublist])) == 1

    def draw(self, surface):
        for y in range(map_height):
            for x in range(map_width):
                pygame.draw.rect(surface,
                                 self.map[y][x].color,
                                 (x * square_size, y * square_size, square_size, square_size)
                                 )
        self.display_info(surface)

    def display_text(self, surface, text, d_x=0):
        image = font.render(text, True, text_color)
        surface.blit(image, (self.x_text + d_x, self.y_text))
        self.y_text += font_size

    def display_color(self, surface, name):
        pygame.draw.rect(surface, game.color[name], (self.x_text, self.y_text, font_size, font_size))

    def display_end(self):
        self.y_text += font_size

    def display_info(self, surface):
        self.y_text = 0

        self.display_text(surface, 'FPS: {}'.format(fps))
        self.display_end()

        self.display_text(surface, 'Population:')
        civ_counter = Counter([item.id for sublist in self.map for item in sublist])
        info = list(sorted(civ_counter.items(), key=lambda x: x[1], reverse=True))
        for c in info:
            self.display_color(surface, c[0])
            self.display_text(surface, str(c[1]), d_x=font_size)
        self.display_end()

        self.display_text(surface, 'Power:')
        for c in info:
            if c[0] == 0:
                continue
            self.display_color(surface, c[0])
            self.display_text(surface, '{} %'.format(round(100 * game.power[c[0]])), d_x=font_size)


class GameManager:
    def __init__(self):
        self.n_civ = 5
        self.civilisations = set(range(1, self.n_civ + 1))

        self.color = dict([(c, random_color()) for c in self.civilisations])
        self.color[0] = pygame.Color('black')

        self.power = dict([(c, uniform(0.05, 0.1)) for c in self.civilisations])
        self.power[0] = 0

        self.pause = True
        self.restart = True
        self.world = None

    def Restart(self):
        self.world = Map()
        self.pause = True
        self.draw()

    def make_turn(self):
        for c in self.civilisations:
            self.world.make_turn(c)

    def get_input(self):
        global fps
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            fps = max(fps - 1, 1)
        if keys[pygame.K_RIGHT]:
            fps += 1

    def check_end(self):
        if self.world.check_end():
            self.pause = True

    def draw(self):
        screen.fill(bg_color)
        self.world.draw(screen)

        pygame.display.flip()
        clock.tick(fps)


pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 720
square_size = 10
map_width = 1000 // square_size
map_height = 720 // square_size

fps = 5

bg_color = pygame.Color('grey12')
text_color = pygame.Color('white')
font_size = 30

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Good game!")
font = pygame.font.SysFont(name='calibri', size=font_size)

game = GameManager()
game.Restart()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.pause = not game.pause
            elif event.key == pygame.K_r:
                game.Restart()

    if game.pause:
        continue

    game.get_input()
    game.make_turn()
    game.check_end()
    game.draw()
