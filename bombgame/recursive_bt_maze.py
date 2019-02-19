# recursive_bt_maze.py
#
#     Author: Jens Gansloser
# Created On: 16 Feb 2019

import os
import random
import numpy as np

class RecursiveBTMaze:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.go = {'N': np.array([0, 2]),
                   'E': np.array([2, 0]),
                   'S': np.array([0, -2]),
                   'W': np.array([-2, 0])}
        self.go_half = {key: (0.5 * value).astype(np.int)
            for key, value in self.go.items()}
        self.opposite = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

        # 0: path, 1: wall.
        self.data = np.ones((width, height), dtype=np.int)

    def generate(self):
        index = np.array([random.randint(0, self.height - 1),
                          random.randint(0, self.width - 1)])

        self.gen(index)

        self.random_break(index)

    def gen(self, index):
        end = True

        for direction in self.shuffle_directions():
            new_index = index + self.go[direction]

            if self.cell_valid(new_index) and not self.cell_visited(new_index):
                self.cell_move(index, new_index)
                self.gen(new_index)
                end = False

        # Remove dead ends.
        if end:
            self.random_break(index)

    def random_break(self, index):
        for direction in self.shuffle_directions():
            new_index = index + self.go[direction]

            if self.cell_valid(new_index) and self.cell_value(
            index + self.go_half[direction]) == 1:
                self.cell_move(index, new_index)
                break

    def cell_value(self, index):
        y, x = index
        return self.data[y, x]

    def cell_visited(self, index):
        return self.cell_value(index) != 1

    def cell_valid(self, index):
        y, x = index

        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return False

        return True

    def cell_move(self, index, new_index):
        y, x = new_index
        self.data[y, x] = 0

        y, x = (index + 0.5 * (new_index - index)).astype(np.int)
        self.data[y, x] = 0

    def shuffle_directions(self):
        return random.sample(self.go.keys(), len(self.go.keys()))

    def itermaze(self):
        return self.__iter2d__(self.data)

    @staticmethod
    def __iter2d__(data):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                yield np.array([i, j]), data[i, j]

    def __str__(self):
        data = -1 * np.ones((self.height + 2, self.width + 2))

        out = ''

        wall = '#'
        path = '0'
        border = '+'

        data[1:-1, 1:-1] = self.data

        for index, value in self.__iter2d__(data):
            if index[1] == 0:
                out += os.linesep

            if value == -1:
                out += border
            elif value == 0:
                out += path
            elif value == 1:
                out += wall

        return out
