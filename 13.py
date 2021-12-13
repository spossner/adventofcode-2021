import os
import sys
from collections import defaultdict, deque

OFFSETS = {
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1,)
}


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        read_grid = True
        rows = []
        instr = []
        width = 0
        height = 0
        for row in data:
            if read_grid:
                if row != '':
                    rows.append([int(d) for d in row.split(',')])
                    if rows[-1][0] >= width:
                        width = rows[-1][0]+1
                    if rows[-1][1] >= height:
                        height = rows[-1][1]+1
                else:
                    read_grid = False
            else:
                instr.append(row[11:].split('='))
        grid = [['.'] * width for _ in range(height)]
        for row in rows:
            grid[row[1]][row[0]] = '#'
        print(width, height)
        self.dump(grid)
        for cmd in instr:
            if cmd[0] == 'x':
                grid = self.fold_x(grid, int(cmd[1]))
            else:
                grid = self.fold_y(grid, int(cmd[1]))
            self.dump(grid)

        count = 0
        for row in grid:
            count += sum(1 if c == '#' else 0 for c in row)
        return count


    def dump(self, grid):
        for row in grid:
            print(''.join(row))
        print()

    # 0 1 2 3 4 | 6 7 8 9 10
    def fold_x(self, grid, fx):
        for row in grid:
            for x in range(1, fx+1):
                if fx + x >= len(grid[0]):
                    break
                if row[fx+x] == '#':
                    row[fx-x] = '#'
        for i in range(len(grid)):
            grid[i] = grid[i][0:fx]
        return grid

    # 0 1 2 3 4 | 6 7 8 9 10
    def fold_y(self, grid, fy):
        for y in range(1, fy + 1):
            if fy + y >= len(grid):
                break
            for x in range(len(grid[0])):
                if grid[fy + y][x] == '#':
                    grid[fy - y][x] = '#'
        return grid[0:fy]


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
