# game.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import tilemap
from . import maze
import sys
import os.path

def run():
    root_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    stone_file = os.path.join(root_dir, 'bombgame/assets/stoneblock.png')
    grass_file = os.path.join(root_dir, 'bombgame/assets/grass.png')

    pygame.init()

    # create pygame window
    screen = pygame.display.set_mode((600, 600))

    # create tile map
    map = tilemap.TileMap((20, 20), (30, 30))
    maze.generate(map)

    # load assets
    bg_sprites = [pygame.image.load(grass_file),
        pygame.image.load(stone_file)]

    done = False

    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True

        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP]:
        #     y -= 3
        # if pressed[pygame.K_DOWN]:
        #     y += 3
        # if pressed[pygame.K_LEFT]:
        #     x -= 3
        # if pressed[pygame.K_RIGHT]:
        #     x += 3

        screen.fill((0, 0, 0))

        width, height = map.size
        twidth, theight = map.tileSize
        for y in range(height):
            for x in range(width):
                bg = map.background[y, x]
                real_pos = (x * twidth, y * theight)
                rect = pygame.Rect(real_pos, (twidth, theight))
                screen.blit(bg_sprites[bg], rect)

        pygame.display.flip()
        clock.tick(60)
