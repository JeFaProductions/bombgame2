# maze.py

from . import tilemap
import random

def generate(map):
    width, height = map.size

    for y in range(height):
        for x in range(width):
            tile = map[x, y]
            bgtype = random.randint(0, 1)

            tile.background_type = bgtype
            if bgtype == tilemap.STONEBLOCK:
                tile.blocked = True
