import os
import sys
from collections import deque
from functools import total_ordering
import bisect

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}

@total_ordering
class Node:
    def __init__(self, x, y, distance):
        self.x = x
        self.y = y
        self.distance = distance

    def __lt__(self, other):
        if self.distance == other.distance:
            if self.x != other.x:
                return self.x < other.x
            else:
                return self.y < other.y
        return self.distance < other.distance

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.distance == other.distance

    def __hash__(self):
        return self.__str__().__hash__()

    def __str__(self):
        return f"({self.x},{self.y} | {self.distance})"


class Solution:
    def __init__(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        self.grid = [[int(d) for d in row] for row in data]
        self.modified = modified
        self.tile_width = len(self.grid[0])
        self.tile_height = len(self.grid)

    def get_width(self):
        return self.tile_width if not self.modified else self.tile_width * 5

    def get_height(self):
        return self.tile_height if not self.modified else self.tile_height * 5

    def get_costs(self, x, y):
        if self.modified:
            tile_x = int(x / self.tile_width)
            tile_y = int(y / self.tile_height)
            costs = self.grid[y % self.tile_height][x % self.tile_width] + tile_x + tile_y
            while costs > 9:
                costs -= 9
            return costs
        return self.grid[y][x]

    def inside_grid(self, x, y):
        assert self.grid
        return 0 <= x < self.get_width() and 0 <= y < self.get_height()

    def solve(self):
        dist = []

        for y in range(self.get_height()):
            dist.append([sys.maxsize] * self.get_width())

        self.dump_grid()

        stack = deque()
        stack.append(Node(0, 0, 0))
        dist[0][0] = 0  # self.grid[0][0]

        max_w = 0
        max_h = 0

        while stack:
            n = stack.popleft()
            for dx, dy in DIRECT_ADJACENTS:
                x = n.x + dx
                y = n.y + dy
                if not self.inside_grid(x, y):
                    continue

                new_dist = dist[n.y][n.x] + self.get_costs(x, y)
                if dist[y][x] > new_dist:
                    if dist[y][x] != sys.maxsize:
                        delete = Node(x, y, dist[y][x])
                        if delete in stack:
                            stack.remove(delete)
                    dist[y][x] = new_dist
                    bisect.insort(stack, Node(x, y, new_dist))

        return dist[-1][-1]

    def dump_grid(self):
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                print(f"{self.get_costs(x, y):<1}", end='')
            print()
        print()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")

    with open(f'{script}-dev.txt') as f:
        s = Solution(f.read().strip().splitlines(), True)
        result = s.solve()
        print(result)

    # with open(f'{script}.txt') as f:
    #     s = Solution(f.read().strip().splitlines(), True)
    #     result = s.solve()
    #     print(result)
