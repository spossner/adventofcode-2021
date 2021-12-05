import os
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        grid = defaultdict(int)
        width = height = 0
        for row in data:
            a = row.split('->')
            x1, y1 = (int(p) for p in a[0].split(','))
            x2, y2 = (int(p) for p in a[1].split(','))
            width = max(width, x1, x2)
            height = max(height, y1, y2)

            if not modified and x1 != x2 and y1 != y2:
                continue

            # 1,2 -> 1,0
            # dx = 0
            # dy = -2
            steps = max(abs(x2-x1), abs(y2-y1))

            dx = int((x2 - x1) / steps)
            dy = int((y2 - y1) / steps)
            p = (x1, y1)
            for i in range(steps+1):
                grid[p] += 1
                p = (p[0]+dx, p[1]+dy)


        self.dump(grid, width, height)
        count = 0
        for v in grid.values():
            if v > 1:
                count += 1

        return count

    def dump(self, grid, w, h):
        for y in range(h):
            for x in range(w):
                print(f"{grid[(x,y)]:<3}", end='')
            print()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)


