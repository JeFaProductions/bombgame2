# game_logic.py
#
# Author: Fabian Meyer
# Created On: 21 Feb 2019

import numpy as np
from . import objects

def update(map, players, bombs, explosions):
    place_bombs(players, bombs, map)
    move_players(players, map)
    update_explosions(explosions, map)
    update_bombs(bombs, map, explosions)
    process_hits(players, map)


def place_bombs(players, bombs, map):
    for player in players:
        # check if the drop bomb flag is set and bomb limit is not
        # exceeded
        if player.drop_bomb and player.bomb_count < player.max_bombs and \
           not map.is_blocked(player.pos):
            # create a new bomb
            bomb = objects.Bomb(pos=player.pos, owner=player)
            bombs.append(bomb)
            # a bomb blocks a tile
            map.set_blocked(bomb.pos, True)
            # disable bomb flag and increment count
            player.drop_bomb = False
            player.bomb_count += 1

def move_players(players, map):
    for player in players:
        # calculate new player position
        new_pos = player.pos + player.move
        # check if the new player position is a valid target
        if map.is_valid(new_pos) and not map.is_blocked(new_pos):
            player.pos = new_pos

def update_bombs(bombs, map, explosions):
    # keep track of the exploded bombs
    exploded = []
    for i, bomb in enumerate(bombs):
        # if the timer reaches zero the bomb explodes
        if bomb.time == 0:
            exploded.append(i)
            map.set_blocked(bomb.pos, False)
            bomb.owner.bomb_count -= 1
        else:
            bomb.time -= 1

    # revert index list such that all indices stay valid during removal
    exploded.reverse()
    for i in exploded:
        pos = bombs[i].pos
        bomb_range = bombs[i].range
        owner = bombs[i].owner

        # add a new explosion at the position of the bomb
        explosions.append(objects.Explosion(pos=pos, owner=owner))
        map.set_explosion(pos, explosions[-1])

        # define the four diections west, east, south, north
        directions = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
        for dir in directions:
            # try to spread the explosions as far as possible
            for delta in range(1, bomb_range):
                npos = pos + dir * delta

                # check if the position is valid, if not stop explosion spread
                # here
                if not map.is_valid(npos) or map.is_blocked(npos) or \
                   map.has_explosion(npos):
                    break

                # add a new explosion at the position
                explosions.append(objects.Explosion(pos=npos, owner=owner))
                map.set_explosion(npos, explosions[-1])

        del bombs[i]

def update_explosions(explosions, map):
    # keep track of the explosions that should be removed
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

def process_hits(players, map):
    killed = []
    for i, player in enumerate(players):
        if map.has_explosion(player.pos):
            explosion = map.get_explosion(player.pos)
            player.lifes -= 1
            explosion.owner.hits += 1
            if player.is_dead():
                explosion.owner.kills += 1
                killed.append(i)

    killed.reverse()
    for i in killed:
        del players[i]
