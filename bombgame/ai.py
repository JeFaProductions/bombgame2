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
        self.weight_enemy = 5
        self.weight_crossroad = 6

    def update(self, world):
        if self.state == SEARCH_TARGET:
            score = np.zeros(world.map.size)
            unblock = ~world.map.blocked
            width, height = score.shape

            positions = np.empty((width, height, 2))
            positions[:, :, 0] = np.arange(width).reshape(1, width).repeat(height, 0)
            positions[:, :, 1] = np.arange(height).reshape(height, 1).repeat(width, 1)

            self_dist = np.abs(positions - self.player.pos).sum(2)
            self_dist /= self_dist.max()
            self_dist -= 1
            self_dist *= -1

            if len(world.players) > 1:
                enemy_dist = []
                for enemy in world.players:
                    if enemy.id != self.player.id:
                        enemy_dist.append(np.abs(positions - enemy.pos).sum(2))
                enemy_dist = np.min(np.array(enemy_dist), axis=0)
                enemy_dist /= enemy_dist.max()
                enemy_dist -= 1
                enemy_dist *= -1
            else:
                enemy_dist = np.zeros((width, height))

            crossroads = np.zeros((width, height))
            crossroads[1:, :] += unblock[:-1, :] * 1
            crossroads[:-1, :] += unblock[1:, :] * 1
            crossroads[:, 1:] += unblock[:, :-1] * 1
            crossroads[:, :-1] += unblock[:, 1:] * 1
            crossroads /= 4

            score += self.weight_self * self_dist
            score += self.weight_enemy * enemy_dist
            score += self.weight_crossroad * crossroads
            score[world.map.blocked] = 0

            target = np.unravel_index(np.argmax(score), score.shape)

            def is_valid(node, path):
                return world.map.is_valid(node) and not world.map.is_blocked(node)

            self.path = astar.search(self.player.pos, target, is_valid=is_valid)
            if self.path:
                self.state = MOVE
            else:
                print('No path found')
        elif self.state == MOVE:
            if self.path:
                next_pos = self.path.pop(0)
                self.player.move = np.array(next_pos, dtype=np.int) - self.player.pos
            else:
                self.player.drop_bomb = True
                self.state = SEARCH_TARGET
