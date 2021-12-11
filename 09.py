import os
import sys
from collections import defaultdict, deque

COLORS = {
    0: u"\u001b[38;5;0m",
    1: u"\u001b[38;5;17m",
    2: u"\u001b[38;5;19m",
    3: u"\u001b[38;5;21m",
    4: u"\u001b[38;5;26m",
    5: u"\u001b[38;5;30m",
    6: u"\u001b[38;5;38m",
    7: u"\u001b[38;5;44m",
    8: u"\u001b[38;5;50m",
    9: u"\u001b[38;5;15m",
}


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        grid = []
        for row in data:
            grid.append([int(c) for c in row])
        h = len(grid)
        w = len(grid[0])
        d = []
        for y in range(h):

            for x in range(w):
                v = grid[y][x]
                if v in COLORS:
                    print(COLORS[v],end='')
                print(v, end='')
                if (y == 0 or v < grid[y - 1][x]) and (y == h-1 or v < grid[y + 1][x]) and (x == 0 or v < grid[y][x - 1]) and (x == w-1 or v < grid[y][x + 1]):
                    d.append((x, y))
            print()
        basins = []
        visited = set()
        for p in d:
            b = self.find_basin(grid, p, w, h, visited)
            basins.append(b)
        basins.sort()
        return basins[-1]*basins[-2]*basins[-3]
        # return sum(basins[-3:])

    def find_basin(self, grid, p, w, h, visited):
        if p in visited:
            return 0
        visited.add(p)
        d = deque()
        d.append((p[0], p[1])) # x, y
        b = [p]
        size = 1
        while len(d) > 0:
            for _ in range(len(d)):
                x, y = d.popleft()
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx = x + dx
                    ny = y + dy
                    np = (nx, ny)
                    if nx < 0 or ny < 0 or nx >= w or ny >= h or grid[ny][nx] == 9 or np in visited:
                        continue
                    size += 1
                    b.append(np)
                    d.append(np)
                    visited.add(np)
        #print(f"found {b} with size {size}")
        return size


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)
