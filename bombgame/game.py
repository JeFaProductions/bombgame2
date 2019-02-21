# game.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import objects
from . import maze
import sys
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

    if pressed[pygame.K_SPACE]:
        human.drop_bomb = True

def place_bombs(players, bombs, map):
    for player in players:
        if player.drop_bomb:
            bombs.append(objects.Bomb(pos=player.pos, owner=player))
            map.blocked[player.pos[1], player.pos[0]] = True
            player.drop_bomb = False

def move_players(players, map):
    for player in players:
        new_pos = player.pos + player.move
        if new_pos[0] >= 0 and new_pos[0] < map.size[0] and \
           new_pos[1] >= 0 and new_pos[1] < map.size[1] and \
           not map.blocked[new_pos[1], new_pos[0]]:
            player.pos = new_pos

def draw_tilemap(screen, map, tile_sprites):
    width, height = map.size
    twidth, theight = map.tileSize
    for y in range(height):
        for x in range(width):
            bg = map.background[y, x]
            real_pos = (x * twidth, y * theight)
            rect = pygame.Rect(real_pos, (twidth, theight))
            screen.blit(tile_sprites[bg], rect)

def draw_bombs(screen, bombs, map, sprite):
    twidth, theight = map.tileSize
    for bomb in bombs:
        real_pos = (bomb.pos[0] * twidth, bomb.pos[1] * theight)
        rect = pygame.Rect(real_pos, (twidth, theight))
        screen.blit(sprite, rect)

def draw_players(screen, players, map, player_sprites):
    twidth, theight = map.tileSize
    for player, sprites in zip(players, player_sprites):
        real_pos = (player.pos[0] * twidth, player.pos[1] * theight)
        rect = pygame.Rect(real_pos, (twidth, theight))
        screen.blit(sprites[0], rect)

def run():
    root_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    stone_file = os.path.join(root_dir, 'bombgame/assets/stoneblock.png')
    grass_file = os.path.join(root_dir, 'bombgame/assets/grass.png')
    player_file = os.path.join(root_dir, 'bombgame/assets/player.png')
    bomb_file = os.path.join(root_dir, 'bombgame/assets/bomb.png')

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
    tile_sprites = [pygame.image.load(grass_file),
        pygame.image.load(stone_file)]
    sprite = pygame.image.load(player_file)
    player_sprites = [[sprite] for _ in players]
    bomb_sprite = pygame.image.load(bomb_file)

    done = False

    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True

        process_human_input(human)
        place_bombs(players, bombs, map)
        move_players(players, map)

        screen.fill((0, 0, 0))

        draw_tilemap(screen, map, tile_sprites)
        draw_bombs(screen, bombs, map, bomb_sprite)
        draw_players(screen, players, map, player_sprites)

        pygame.display.flip()
        clock.tick(10)
