# game.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import pygame
from . import objects
from . import maze
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

    if pressed[pygame.K_SPACE]:
        human.drop_bomb = True

def place_bombs(players, bombs, map):
    for player in players:
        if player.drop_bomb and player.bomb_count < player.max_bombs:
            bombs.append(objects.Bomb(pos=player.pos, owner=player))
            map.set_blocked(player.pos, True)
            player.drop_bomb = False
            player.bomb_count += 1

def move_players(players, map):
    for player in players:
        new_pos = player.pos + player.move
        if map.is_valid(new_pos) and not map.is_blocked(new_pos):
            player.pos = new_pos

def update_bombs(bombs, map, explosions):
    exploded = []
    for i, bomb in enumerate(bombs):
        if bomb.time == 0:
            exploded.append(i)
            map.set_blocked(bomb.pos, False)
            bomb.owner.bomb_count -= 1
        else:
            bomb.time -= 1

    exploded.reverse()
    for i in exploded:
        pos = bombs[i].pos
        bomb_range = bombs[i].range
        owner = bombs[i].owner

        explosions.append(objects.Explosion(pos=pos, owner=owner))
        map.set_explosion(pos, explosions[-1])

        directions = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
        for dir in directions:
            for delta in range(1, bomb_range):
                npos = pos + dir * delta

                if not map.is_valid(npos) or map.is_blocked(npos) or \
                   map.has_explosion(npos):
                    break

                explosions.append(objects.Explosion(pos=npos, owner=owner))
                map.set_explosion(npos, explosions[-1])

        del bombs[i]

def update_explosions(explosions, map):
    to_remove = []
    for i, explosion in enumerate(explosions):
        if explosion.time == 0:
            to_remove.append(i)
            map.set_explosion(explosion.pos, None)
        else:
            explosion.time -= 1

    to_remove.reverse()
    for i in to_remove:
        del explosions[i]

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
            place_bombs(players, bombs, map)
            move_players(players, map)
            update_explosions(explosions, map)
            update_bombs(bombs, map, explosions)

        screen.fill((0, 0, 0))

        draw_tilemap(screen, map, sprites['tiles'])
        # draw explosions
        draw_objects(screen, explosions, map, sprites['explosion'])
        # draw bombs
        draw_objects(screen, bombs, map, sprites['bomb'])
        draw_players(screen, players, map, sprites['player'])

        pygame.display.flip()
        timeAccount += clock.tick(60)
