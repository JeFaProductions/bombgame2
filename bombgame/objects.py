# tilemap.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import numpy as np

class TileMap:
    def __init__(self, size, tileSize):
        self.size = size
        self.tileSize = tileSize
        width, height = size
        self.background = np.zeros((height, width), dtype=np.int)
        self.blocked = self.background == 0

class Bomb:
    def __init__(self, pos=np.array((0, 0)), time=10, owner=None):
        self.pos = pos
        self.time = time
        self.owner = owner

class Player:
    def __init__(self, pos=np.array((0, 0)), lifes=1, kills=0):
        self.pos = pos
        self.lifes = lifes
        self.kills = kills
        self.move = np.array((0, 0))
        self.drop_bomb = False

    def is_dead(self):
        return self.lifes == 0
