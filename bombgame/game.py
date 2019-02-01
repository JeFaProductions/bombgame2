# game.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import tilemap
from . import maze

def run():
    pygame.init()

    # create pygame window
    screen = pygame.display.set_mode((600, 600))

    # create tile map
    map = tilemap.TileMap((20, 20), (30, 30))
    maze.generate(map)

    # load assets
    stoneblock_img = pygame.image.load('assets/stoneblock.png')
    grass_img = pygame.image.load('assets/grass.png')

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
                tile = map[x, y]
                real_pos = (x * twidth, y * theight)
                rect = pygame.Rect(real_pos, tile.size)
                if tile.background_type == tilemap.GRASS:
                    screen.blit(grass_img, rect)
                elif tile.background_type == tilemap.STONEBLOCK:
                    screen.blit(stoneblock_img, rect)

        pygame.display.flip()
        clock.tick(60)
