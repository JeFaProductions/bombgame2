# astar.py
#
# Author: Fabian Meyer
# Created On: 21 Feb 2019

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
    return abs(src[0] - tgt[0]) + abs(src[1] - tgt[1])

def reconstruct_path(node, nodes):
    path = [node.pos]
    while node.came_from is not None:
        node = nodes[node.came_from]
        path.append(node.pos)
    path = path[:-1]
    path.reverse()

    return path

def search(start, target, is_valid=None, maxit=0):
    start = (start[0], start[1])
    target = (target[0], target[1])
    if start == target:
        return []
    if not is_valid(target, []):
        return []

    nodes = {start: Node(pos=start,
        heuristic=manhatten_distance(start, target))}

    path = []
    openlist = [nodes[start]]

    iterations = 0
    found = False
    while not found and openlist and (maxit <= 0 or iterations < maxit):
        # get node with lowest cost
        curr_node = heappop(openlist)
        curr_pos = curr_node.pos

        # check if retrieved node is the target
        if curr_pos == target:
            found = True
            # reconstruct path
            path = reconstruct_path(curr_node, nodes)
        else:
            iterations += 1
            curr_node.closed = True

            # define neughbours by 4-fold neighbourhood
            neighs = [(curr_pos[0] - 1, curr_pos[1]),
                (curr_pos[0] + 1, curr_pos[1]),
                (curr_pos[0], curr_pos[1] - 1),
                (curr_pos[0], curr_pos[1] + 1)]

            for neigh_pos in neighs:
                x, y = neigh_pos
                # check if this neighbour is valid
                if is_valid(neigh_pos, reconstruct_path(curr_node, nodes)):
                    # check if node was already visited before
                    first_visit = neigh_pos not in nodes
                    if first_visit:
                        # add new node since it does not exist yet
                        nodes[neigh_pos] = Node(pos=neigh_pos,
                            heuristic=manhatten_distance(neigh_pos, target))
                    neigh = nodes[(x, y)]

                    # check if neighbour is already in closed list
                    if not neigh.closed:
                        neigh_cost = curr_node.cost + 1
                        is_improvement = neigh_cost < neigh.cost
                        # if this is either the first visit or an improvement
                        # update the path so far
                        if first_visit or is_improvement:
                            neigh.came_from = curr_pos
                            neigh.cost = neigh_cost
                        # if it is the first visit add to open list
                        if first_visit:
                            heappush(openlist, neigh)
                        # if this is an improvement the node is already in
                        # openlist, but total cost has changed
                        if is_improvement:
                            heapify(openlist)
    return path
