from __future__ import nested_scopes

import itertools
import operator
import os
import random
import sys
from bisect import bisect_left
from collections import deque, defaultdict, namedtuple, Counter
from copy import copy
from functools import total_ordering, reduce, lru_cache
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
    def __init__(self, data=None, modified=False, do_splitlines=True, split_char=None):
        if data and do_splitlines:
            data = data.splitlines()
        if data and split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self, p0, p1):
        return max(self.roll((p0 - 1, p1 - 1), (0, 0), 0, 0, is_p0) for is_p0 in (True, False))

    @lru_cache(maxsize=None)
    def roll(self, pos, score, die_sum, count, is_p0):
        if count > 0 and count % 3 == 0:
            # 3 rolls complete ==> update position and score
            if count % 2 != 0:
                pos = ((pos[0] + die_sum) % 10, pos[1])
                score = (score[0] + pos[0] + 1, score[1])
            else:
                pos = (pos[0], (pos[1] + die_sum) % 10)
                score = (score[0], score[1] + pos[1] + 1)
            die_sum = 0

            if score[0] >= 21:
                return 1 if is_p0 else 0
            if score[1] >= 21:
                return 0 if is_p0 else 1

        return sum(self.roll(pos, score, die_sum + die + 1, count + 1, is_p0) for die in range(3))


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = None

    # with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
    #     s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
    #     result = s.solve(4, 8)
    #     print(result)
    #     assert result == 444356092776315
        # print(s.solve(1, 6))

    s = Solution()
    result = s.solve(1, 6)
    print(result)
    # assert result == 444356092776315
