# game.py
#
# Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import objects
from . import maze
from . import game_logic
from . import game_rendering
from . import ai
import os.path
import numpy as np

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
          (0, 255, 255), (255, 0, 255), (255, 255, 255), (0, 0, 0)]

LOGIC_INTERVAL = 100.0


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


def spawn_points(map):
    width, height = map.size
    return [(0, 0), (width - 1, 0),
            (0, height - 1), (width - 1, height - 1),
            (0, int(height / 2)), (int(width / 2), 0),
            (width - 1, int(height / 2)), (int(width / 2), height - 1)]


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
            player.pos = np.array(point, dtype=np.int)
        else:
            neighs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for n in neighs:
                npos = (point[0] + n[0], point[1] + n[1])
                if npos not in visited and map.is_valid(npos):
                    points.append(npos)


def recolor_player(sprite, id):
    result = sprite.copy()

    tmp = pygame.surfarray.pixels3d(result)
    tmp_mask = tmp == 255
    tmp_mask = np.logical_and(tmp_mask[:, :, 0], tmp_mask[:, :, 2])

    tmp[tmp_mask] = np.array(COLORS[id])

    return result


def run():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    asset_dir = os.path.join(root_dir, 'assets')

    stone_file = os.path.join(root_dir, 'assets/stoneblock.png')
    grass_file = os.path.join(root_dir, 'assets/grass.png')
    bomb_file = os.path.join(root_dir, 'assets/bomb.png')
    explosion_file = os.path.join(root_dir, 'assets/explosion.png')

    pygame.init()

    grid_size = (19, 19)
    tile_size = (30, 30)
    screen_size = (grid_size[0] * tile_size[0], grid_size[1] * tile_size[1])

    # create pygame window
    screen = pygame.display.set_mode(screen_size)

    # create tile map
    world = objects.World()
    world.map = objects.TileMap(grid_size, tile_size)
    maze.generate(world.map)

    world.players = [objects.Player(i) for i in range(4)]
    spawns = spawn_points(world.map)
    for s, p in zip(spawns, world.players):
        find_spawn_point(s, p, world.map)
    world.bombs = []
    world.explosions = []
    human = world.players[0]
    ais = [ai.AI(p) for p in world.players[1:]]

    for sname in ['stand', 'walk_up', 'walk_down', 'walk_left', 'walk_right']:
        fname = os.path.join(asset_dir, sname + '.png')
        sprite = pygame.image.load(fname)
        for p in world.players:
            p.sprites[sname] = recolor_player(sprite, p.id)

    # load assets
    sprites = {}
    sprites['tiles'] = [pygame.image.load(grass_file),
                        pygame.image.load(stone_file)]
    sprites['bomb'] = pygame.image.load(bomb_file)
    sprites['explosion'] = pygame.image.load(explosion_file)

    done = False

    clock = pygame.time.Clock()
    timeAccount = 0.0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        process_human_input(human)

        while timeAccount >= LOGIC_INTERVAL:
            # update game logic
            game_logic.update(world)
            # execute all ai based on updated world
            for a in ais:
                a.update(world)
            # reduce time account
            timeAccount -= LOGIC_INTERVAL

        if screen is not None:
            # calculate the render position for each player
            for player in world.players:
                diff = player.pos - player.prev_pos
                fac = max(0.0, timeAccount / LOGIC_INTERVAL)

                # move the sprite according to the amount
                player.render_pos = player.prev_pos + fac * diff
            game_rendering.render(screen, world, sprites)

        timeAccount += clock.tick(60)
