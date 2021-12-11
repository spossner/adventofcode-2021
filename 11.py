import os
import sys
from collections import defaultdict, deque

OFFSETS = {
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1,)
}


class Solution:
    def dump_grid(self, grid):
        for row in grid:
            print(''.join([str(c) for c in row]))

    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        grid = [[int(d) for d in row] for row in data]
        WIDTH = len(grid[0])
        HEIGHT = len(grid)
        print('Before any steps:')
        self.dump_grid(grid)
        flashes = 0
        d = deque()
        for i in range(100000):
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    grid[y][x] += 1
                    if grid[y][x] == 10: # exactly once when passing 10
                        flashes += 1
                        d.append((x,y))
            while d:
                x, y = d.popleft()
                for dx, dy in OFFSETS:
                    nx = x + dx
                    ny = y + dy
                    if nx < 0 or ny < 0 or nx >= WIDTH or ny >= HEIGHT:
                        continue
                    grid[ny][nx] += 1
                    if grid[ny][nx] == 10:
                        flashes += 1
                        d.append((nx, ny))

            active = 0
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if grid[y][x] >= 10:
                        grid[y][x] = 0
                        active += 1

            print(f"\nAfter step {i+1}:")
            self.dump_grid(grid)

            if modified:
                if active == HEIGHT*WIDTH:
                    return i+1
            elif i >= 100:
                return flashes

        return flashes


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    # with open(f'{script}-dev.txt') as f:
    #     result = s.solve(f.read().strip().splitlines(), True)
    #     print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)
