# tilemap.py
#
#     Author: Fabian Meyer
# Created On: 01 Feb 2019

GRASS = 0
STONEBLOCK = 1

class Tile:
    def __init__(self, size):
        self.size = size
        self.background_type = GRASS
        self.blocked = False
        self.object = None


class TileMap:
    def __init__(self, size, tileSize):
        self.size = size
        self.tileSize = tileSize
        width, height = size
        self.tiles = [Tile(tileSize) for _ in range(width * height)]

    def __getitem__(self, key):
        x, y = key
        assert(y >= 0 and y < self.size[1])
        assert(x >= 0 and x < self.size[0])
        idx = y * self.size[0] + x
        return self.tiles[idx]
