# ai.py
#
# Author: Fabian Meyer
# Created On: 21 Feb 2019

import numpy as np
from . import astar

SEARCH_TARGET = 0
MOVE = 1

class AI:
    def __init__(self, player):
        self.player = player
        self.path = []
        self.state = SEARCH_TARGET
        self.weight_self = 3
        self.weight_enemy = 6
        self.weight_crossroad = 3
        self.map_positions = np.empty((0, 0))
        self.bomb_times = np.empty((0, 0))

    def __update_map_positions(self, map):
        if map.size != self.map_positions.shape:
            width, height = map.size
            self.map_positions = np.empty((width, height, 2))
            self.map_positions[:, :, 0] = np.arange(width) \
                .reshape(1, width).repeat(height, 0)
            self.map_positions[:, :, 1] = np.arange(height) \
                .reshape(height, 1).repeat(width, 1)

    def __update_bomb_times(self, bombs, map):
        if map.size != self.bomb_times.shape:
            self.bomb_times = np.empty(map.size, dtype=np.int)

        self.bomb_times[:, :] = 1e16
        # define the four diections west, east, south, north
        directions = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
        for bomb in bombs:
            pos = bomb.pos
            self.bomb_times[pos[0], pos[1]] = bomb.time
            for dir in directions:
                # try to spread the explosions as far as possible
                for delta in range(1, bomb.range):
                    npos = pos + dir * delta
                    # check if the position is valid, if not stop explosion
                    # spread here
                    if not map.is_valid(npos) or map.is_blocked(npos) or \
                       map.has_explosion(npos):
                        break
                    self.bomb_times[pos[0], pos[1]] = bomb.time

    def update(self, world):
        self.player.drop_bomb = False
        self.player.move[:] = 0
        if self.state == SEARCH_TARGET:
            # init score board, each tile gets a score the maximum is chosen as
            # target
            score = np.zeros(world.map.size)
            # get mask of tiles which are not blocked
            unblock = ~world.map.blocked
            width, height = score.shape

            # create array of tile positions, create lazily
            self.__update_map_positions(world.map)
            self.__update_bomb_times(world.bombs, world.map)

            # calculate distances of this player to all other tiles (manhatten)
            self_dist = np.abs(self.map_positions - self.player.pos).sum(2)
            # normalize distances into interval [0,1]
            self_dist /= self_dist.max()
            # make shortest distances have greates value
            self_dist -= 1
            self_dist *= -1

            # check if there are any other players than this one
            if len(world.players) > 1:
                # calculate distances of all enemies to all other tiles
                enemy_dist = []
                for enemy in world.players:
                    # check if this player is not the one controlled by ai
                    if enemy.id != self.player.id:
                        diff = self.map_positions - enemy.pos
                        dist = np.abs(diff).sum(2)
                        enemy_dist.append(dist)

                # convert distance to numpy array
                enemy_dist = np.array(enemy_dist)
                # find element wise minimum of all player distances
                enemy_dist = np.min(enemy_dist, axis=0)
                # normalize distances into interval [0,1]
                enemy_dist /= enemy_dist.max()
                # make shortest distances have greates value
                enemy_dist -= 1
                enemy_dist *= -1
            else:
                # no enemies, distances are zero
                enemy_dist = np.zeros((width, height))

            # detect how many neighbouring unblocked tiles each tile has
            crossroads = np.zeros((width, height))
            # add +1 if left neighbour is not blocked
            crossroads[1:, :] += unblock[:-1, :] * 1
            # add +1 if right neighbour is not blocked
            crossroads[:-1, :] += unblock[1:, :] * 1
            # add +1 if upper neighbour is not blocked
            crossroads[:, 1:] += unblock[:, :-1] * 1
            # add +1 if lower neighbour is not blocked
            crossroads[:, :-1] += unblock[:, 1:] * 1
            # normalize into interval [0,1]
            crossroads /= 4

            # calculate score as weighted sum
            score += self.weight_self * self_dist
            score += self.weight_enemy * enemy_dist
            score += self.weight_crossroad * crossroads
            # set all blocked tiles to zero
            score[world.map.blocked] = 0

            def is_valid(node, path):
                return world.map.is_valid(node) and \
                    not world.map.is_blocked(node) and \
                    not world.map.has_explosion(node) and \
                    self.bomb_times[node[0], node[1]] - len(path) - 1 > 0

            found = False
            iterations = 0
            while not found and iterations < 10:
                # retrieve tile with maximum score
                target = np.unravel_index(np.argmax(score), score.shape)
                # set score to 0
                score[target[0], target[1]] = 0

                # search path with astar
                self.path = astar.search(self.player.pos, target,
                    is_valid=is_valid)
                if self.path:
                    self.state = MOVE
                    found = True
                iterations += 1

            if not found:
                print('No path found!')
        elif self.state == MOVE:
            if self.path:
                next_pos = self.path.pop(0)
                next_pos = np.array(next_pos, dtype=np.int)
                self.player.move = next_pos - self.player.pos
            else:
                self.player.drop_bomb = True
                self.state = SEARCH_TARGET
