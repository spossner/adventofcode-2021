import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}


class Rect: # only for right and below (negative)
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def contains_x(self, x):
        return self.x1 <= x <= self.x2

    def contains_y(self, y):
        return self.y1 >= y >= self.y2

    def contains(self, x, y):
         return self.contains_x(x) and self.contains_y(y)

# target area: x=179..201, y=-109..-63
class Solution:
    def __init__(self, data, modified=False, do_splitlines=True):
        self.data = data.splitlines() if do_splitlines else data
        self.modified = modified
        self.rect = Rect(179, -63, 201, -109)

    def for_x(self, dx, x=0):
        i = 0
        yield x
        while x <= self.rect.x2 and i < 250:
            x += dx
            if dx > 0:
                dx -= 1
            i += 1
            yield x


    def for_y(self, dy, y=0):
        yield y
        while y >= self.rect.y2:
            y += dy
            dy -= 1
            yield y

    def solve(self):
        candidates_x = defaultdict(list)
        candidates_y = defaultdict(list)
        for dx in range(10,210):
            for i, x in enumerate(self.for_x(dx)):
                if self.rect.contains_x(x):
                    candidates_x[i].append(dx)
        for dy in range(300,-300,-1):
            for i, y in enumerate(self.for_y(dy)):
                if self.rect.contains_y(y):
                    candidates_y[i].append(dy)

        results = set()
        max_y = 0
        for i, x_values in candidates_x.items():
            if i in candidates_y:
                y_values = candidates_y[i]

                print(i, x_values, y_values)
                for x in x_values:
                    for y in y_values:
                        if y > max_y:
                            max_y = y
                        results.add((x,y))

        print(f"PART 1: {max(list(self.for_y(max_y)))}")
        print(f"PART 2: {len(results)}")

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    PART2 = True
    SPLIT_LINES = True

    with open(f'{script}-dev.txt') as f:
        Solution(f.read().strip(), PART2, SPLIT_LINES).solve()

        # 3760 -> tooo high.. mmhh
        # 1711 too low

    # with open(f'{script}.txt') as f:
    #     s = Solution(f.read().strip(), PART2, SPLIT_LINES)
    #     result = s.solve()
    #     print(result)
