# game.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import objects
from . import maze
from . import game_logic
import os.path

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

def draw_players(screen, players, map, player_sprites):
    draw_objects(screen, players, map, player_sprites[0])

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
    map = objects.TileMap((20, 20), (30, 30))
    maze.generate(map)

    players = [objects.Player()]
    bombs = []
    explosions = []
    human = players[0]
    # ais = players[1:]

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
            game_logic.update(map, players, bombs, explosions)

        screen.fill((0, 0, 0))

        draw_tilemap(screen, map, sprites['tiles'])
        # draw explosions
        draw_objects(screen, explosions, map, sprites['explosion'])
        # draw bombs
        draw_objects(screen, bombs, map, sprites['bomb'])
        draw_players(screen, players, map, sprites['player'])

        pygame.display.flip()
        timeAccount += clock.tick(60)
