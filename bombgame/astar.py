# astar.py
#
# Author: Fabian Meyer
# Created On: 21 Feb 2019

import math
from heapq import heappop, heappush, heapify

class Node:
    def __init__(self, pos=(0, 0), heuristic=0, closed=False, cost=0):
        self.cost = cost
        self.heuristic = heuristic
        self.pos = pos
        self.closed = closed
        self.came_from = None

    def total_cost(self):
        return self.cost + self.heuristic

    def __lt__(self, other):
        return self.total_cost() < other.total_cost()

    def __le__(self, other):
        return self.total_cost() <= other.total_cost()

def manhatten_distance(src, tgt):
    return math.abs(src[0] - tgt[0]) + math.abs(src[1] - tgt[1])

def search(start, target, map, maxit=0):
    start = (start[0], start[1])
    target = (target[0], target[1])
    if start == target:
        return [], 0
    if target[0] < 0 or target[0] >= map.width or \
       target[1] < 0 or target[1] >= map.height or \
       map.blocked[target[0], target[1]]:
        return [], 0

    nodes = {start: Node(pos=start,
        heuristic=manhatten_distance(start, target))}

    path = []
    openlist = [nodes[start]]

    iterations = 0
    found = False
    while not found and openlist and (maxit <= 0 or iterations < maxit):
        # get node with lowest cost
        currNode = heappop(openlist)
        currPos = currNode.pos

        # check if retrieved node is the target
        if currPos == target:
            # reconstruct path
            path = [target]
            while currNode.came_from is not None:
                currNode = nodes[currNode.came_from]
                path.append(currNode.pos)
            path = path.reverse()
            found = True
        else:
            iterations += 1
            currNode.closed = True

            # define neughbours by 4-fold neighbourhood
            neighs = [(currPos[0] - 1, currPos[1]),
                (currPos[0] + 1, currPos[1]),
                (currPos[0], currPos[1] - 1),
                (currPos[0], currPos[1] + 1)]

            for neighPos in neighs:
                x, y = neighPos
                # check if this neighbours lies within the map and is not
                # blocked
                valid = x >= 0 and x < map.width and \
                    y >= 0 and y < map.height and \
                    not map.blocked[y, x]
                if valid:
                    # check if node was already visited before
                    firstVisit = neighPos not in nodes
                    if firstVisit:
                        # add new node since it does not exist yet
                        nodes[neighPos] = Node(pos=neighPos,
                            heuristic=manhatten_distance(neighPos, target))
                    neigh = nodes[(x, y)]

                    # check if neighbour is already in closed list
                    if not neigh.closed:
                        neighCost = currNode.cost + 1
                        isImprovement = neighCost < neigh.cost
                        # if this is either the first visit or an improvement
                        # update the path so far
                        if firstVisit or isImprovement:
                            neigh.came_from = currPos
                            neigh.cost = neighCost
                        # if it is the first visit add to open list
                        if firstVisit:
                            heappush(openlist, neigh)
                        # if this is an improvement the node is already in
                        # openlist, but total cost has changed
                        if isImprovement:
                            heapify(openlist)
    return path, iterations
