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
