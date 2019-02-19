# maze.py

from .recursive_bt_maze import RecursiveBTMaze

def generate(map):
    width, height = map.size

    mazegen = RecursiveBTMaze(width, height)
    mazegen.generate()

    map.blocked[:, :] = mazegen.data == 1
    map.background[:, :] = mazegen.data
