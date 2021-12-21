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


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self, p1, p2):
        pos = [p1 - 1, p2 - 1]  # reduced by 1 to to module
        scores = [0, 0]
        next_player = 0
        next_dice = 1

        count = 0
        while True:
            sum = 3 * next_dice + 3
            next_dice += 3
            count += 3  # count dices
            pos[next_player] = (pos[next_player] + sum) % 10  # BOARD SIZE
            scores[next_player] += pos[next_player] + 1
            if scores[next_player] >= 1000:
                break
            next_player = 1 - next_player

        return count * min(scores)


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
        print(s.solve(1, 6))
        # too high: 27349
        # 5569 too high...
        # wieder 5569... mmmhhhh
        # 5519 (warum?)
        # 5479
        # 5474 mmmh... auch nicht richtig...
        # 5294 too low
