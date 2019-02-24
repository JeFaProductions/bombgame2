# game_rendering.py
#
# Author: Fabian Meyer
# Created On: 21 Feb 2019

import pygame

def render(screen, world, sprites):
    screen.fill((0, 0, 0))

    draw_tilemap(screen, world.map, sprites['tiles'])
    # draw explosions
    draw_objects(screen, world.explosions, world.map, sprites['explosion'])
    # draw bombs
    draw_objects(screen, world.bombs, world.map, sprites['bomb'])
    draw_players(screen, world.players, world.map, sprites['player'])

    pygame.display.flip()

def draw_tilemap(screen, map, tile_sprites):
    width, height = map.size
    twidth, theight = map.tileSize
    for y in range(height):
        for x in range(width):
            bg = map.background[x, y]
            real_pos = (x * twidth, y * theight)
            rect = pygame.Rect(real_pos, (twidth, theight))
            screen.blit(tile_sprites[bg], rect)

def draw_objects(screen, objects, map, sprite):
    twidth, theight = map.tileSize
    for obj in objects:
        real_pos = (obj.pos[0] * twidth, obj.pos[1] * theight)
        rect = pygame.Rect(real_pos, (twidth, theight))
        screen.blit(sprite, rect)

def draw_players(screen, players, map, sprites):
    for p, s in zip(players, sprites):
        draw_objects(screen, [p], map, s)
