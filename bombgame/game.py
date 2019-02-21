# game.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import objects
from . import maze
from . import game_logic
from . import game_rendering
from . import ai
import os.path
import numpy as np

def process_human_input(human):
    human.move[:] = 0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        human.move[1] = -1
    elif pressed[pygame.K_DOWN]:
        human.move[1] = 1
    elif pressed[pygame.K_LEFT]:
        human.move[0] = -1
    elif pressed[pygame.K_RIGHT]:
        human.move[0] = 1

    human.drop_bomb = False
    if pressed[pygame.K_SPACE]:
        human.drop_bomb = True

def find_spawn_point(start, player, map):
    player.pos = np.array(start, dtype=np.int)
    points = [(start[0], start[1])]
    visited = {}
    found = False
    while not found and points:
        point = points[0]
        points = points[1:]
        visited[point] = True

        if not map.is_blocked(point):
            found = True
            player.pos = point
        else:
            neighs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for n in neighs:
                npos = (point[0] + n[0], point[1] + n[1])
                if npos not in visited and map.is_valid(npos):
                    points.append(npos)

def run():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    stone_file = os.path.join(root_dir, 'assets/stoneblock.png')
    grass_file = os.path.join(root_dir, 'assets/grass.png')
    player_file = os.path.join(root_dir, 'assets/player.png')
    bomb_file = os.path.join(root_dir, 'assets/bomb.png')
    explosion_file = os.path.join(root_dir, 'assets/explosion.png')

    pygame.init()

    # create pygame window
    screen = pygame.display.set_mode((600, 600))

    # create tile map
    world = objects.World()
    world.map = objects.TileMap((20, 20), (30, 30))
    maze.generate(world.map)

    world.players = [objects.Player(i) for i in range(2)]
    find_spawn_point((0, 0), world.players[0], world.map)
    find_spawn_point((0, world.map.size[1] - 1), world.players[1], world.map)
    world.bombs = []
    world.explosions = []
    human = world.players[0]
    ais = [ai.AI(p) for p in world.players[1:]]

    # load assets
    sprites = {}
    sprites['tiles'] = [pygame.image.load(grass_file),
        pygame.image.load(stone_file)]
    sprites['player'] = [pygame.image.load(player_file)]
    sprites['bomb'] = pygame.image.load(bomb_file)
    sprites['explosion'] = pygame.image.load(explosion_file)

    done = False

    clock = pygame.time.Clock()
    timeAccount = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True

        process_human_input(human)
        if timeAccount >= 100:
            timeAccount = 0
            game_logic.update(world)

        if screen is not None:
            game_rendering.render(screen, world, sprites)

        timeAccount += clock.tick(60)
