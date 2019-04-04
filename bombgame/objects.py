# tilemap.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

import numpy as np

class Grid:
    def __init__(self, size, value=None):
        self.size = size
        self.data = [None for _ in range(size[0] * size[1])]

    def __getitem__(self, idx):
        x, y = idx
        idx = y * self.size[0] + x
        return self.data[idx]

    def __setitem__(self, idx, value):
        x, y = idx
        idx = y * self.size[0] + x
        self.data[idx] = value

class TileMap:
    def __init__(self, size, tileSize):
        self.size = size
        self.tileSize = tileSize
        width, height = size
        self.background = np.zeros((width, height), dtype=np.int)
        self.blocked = self.background == 0
        self.explosions = Grid(size)

    def is_valid(self, pos):
        return pos[0] >= 0 and pos[0] < self.size[0] and\
            pos[1] >= 0 and pos[1] < self.size[1]

    def is_blocked(self, pos):
        return self.blocked[pos[0], pos[1]]

    def set_blocked(self, pos, value):
        self.blocked[pos[0], pos[1]] = value

    def has_explosion(self, pos):
        return self.get_explosion(pos) is not None

    def get_explosion(self, pos):
        return self.explosions[pos[0], pos[1]]

    def set_explosion(self, pos, value):
        self.explosions[pos[0], pos[1]] = value


class Explosion:
    def __init__(self, pos=(0, 0), time=10, owner=None):
        self.pos = np.array(pos, dtype=np.int)
        self.time = time
        self.owner = owner

class Bomb:
    def __init__(self, pos=(0, 0), time=10, owner=None, range=3):
        self.pos = np.array(pos, dtype=np.int)
        self.time = time
        self.owner = owner
        self.range = range

class Player:
    def __init__(self, id, pos=(0, 0), lifes=1, kills=0, hits=0,
    max_bombs=5):
        self.id = id
        self.prev_pos = np.array(pos, dtype=np.int)
        self.pos = np.array(pos, dtype=np.int)
        self.render_pos = np.array(pos, dtype=np.float64)
        self.lifes = lifes
        self.kills = kills
        self.hits = hits
        self.move = np.array((0, 0), dtype=np.int)
        self.drop_bomb = False
        self.bomb_count = 0
        self.max_bombs = max_bombs

    def is_dead(self):
        return self.lifes == 0

class World:
    def __init__(self):
        self.map = None
        self.bombs = []
        self.players = []
        self.explosions = []
