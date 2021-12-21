from __future__ import nested_scopes

import operator
import os
import random
import sys
from bisect import bisect_left
from collections import deque, defaultdict, namedtuple
from copy import copy
from functools import total_ordering, reduce
import bisect
from itertools import permutations, combinations

import numpy as np

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))
PIXEL_WITH_NEIGHBOURS = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (0, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1))


class Rect:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x2 = 0
        self.y2 = 0

    def contains(self, x, y):
        return self.x <= x < self.x2 and self.y <= y < self.y2

    def extend(self, x, y):
        self.x = min(self.x, x)
        self.y = min(self.y, y)
        self.x2 = max(self.x2, x + 1)
        self.y2 = max(self.y2, y + 1)

    def iterate(self,offset=0):  # iterate row by row...
        for y in range(self.y+offset, self.y2-offset):
            for x in range(self.x+offset, self.x2-offset):
                yield (x, y)

    def grow(self, i):
        self.x -= i
        self.y -= i
        self.x2 += i
        self.y2 += i

    def __str__(self):
        return f"({self.x},{self.y},{self.x2},{self.y2})"


class InfiniteGrid:
    def __init__(self, rect=None, default=0):
        self.grid = defaultdict(int)
        self.rect = copy(rect) if rect is not None else Rect()
        self.default = default

    def switch_default(self):
        self.default = 1 - self.default
        for x,y in self.iterate():
            if x == self.rect.x or y == self.rect.y or x == self.rect.x2-1 or y == self.rect.y2-1:
                self.grid[(x, y)] = self.default

    def set(self, x, y, v):
        assert v in (0, 1)
        self.rect.extend(x, y)
        self.grid[(x, y)] = v

    def get(self, x, y, graphics=False):
        if not self.rect.contains(x, y):
            if graphics:
                return '#' if self.default == 1 else '.'
            else:
                return self.default
        if graphics:
            return '#' if self.grid[(x, y)] == 1 else '.'
        return self.grid[(x, y)]

    def grow(self, i):
        self.rect.grow(i)

    def iterate(self,offset=0):
        return self.rect.iterate(offset)


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def calc_index(self, img, x, y):
        id = ''
        for dx, dy in PIXEL_WITH_NEIGHBOURS:
            id += str(img.get(x + dx, y + dy))
        return int(id, 2)

    def solve(self):
        replace = list(self.data[0])
        img = InfiniteGrid()
        for y, row in enumerate(self.data[2:]):
            for x, c in enumerate(row):
                img.set(x, y, 1 if c == '#' else 0)
        img.grow(10 if not self.modified else 100)
        self.dump_image(img)
        for r in range(2 if not self.modified else 50):
            new_img = InfiniteGrid(img.rect, img.default)
            for x, y in new_img.iterate(1):
                new_img.set(x, y, 0 if replace[self.calc_index(img, x, y)] == '.' else 1)
            img = new_img
            if replace[0] == '#':
                img.switch_default()
            if r % 10 == 0:
                self.dump_image(img)

        count = 0
        for x, y in img.iterate():
            count += img.get(x, y)
        return count

    def dump_image(self, img, border=0):
        for y in range(img.rect.y - border, img.rect.y2 + border):
            for x in range(img.rect.x - border, img.rect.x2 + border):
                print(img.get(x, y, True), end='')
            print()
        print()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = None

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
        # too high: 27349
        # 5569 too high...
        # wieder 5569... mmmhhhh
        # 5519 (warum?)
        # 5479
        # 5474 mmmh... auch nicht richtig...
        # 5294 too low
