from __future__ import nested_scopes

import operator
import os
import random
import sys
from bisect import bisect_left
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations, combinations

import numpy as np

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))

class Beacon:
    def __init__(self, vec):
        assert vec is not None
        self.vec = np.array(vec)
        self.neighbours = []

    def __str__(self):
        return str(self.vec)

    def __repr__(self):
        return self.__str__()

    def set_neighbours(self, beacons):
        for b in beacons:
            if self != b:
                bisect.insort(self.neighbours, self.distance(b))
        print(self.neighbours)

    def distance(self, other):
        return np.linalg.norm(self.vec-other.vec)

    def intersection_count(self, other):
        result = 0
        for b in self.neighbours:
            i = bisect_left(other.neighbours, b)
            if i != len(other.neighbours) and (other.neighbours[i] - b) < 0.000001:
                result += 1
        return result


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        current_scanner = None
        scanners = defaultdict(list)
        for row in self.data:
            if len(row) == 1:
                s = row[0]
                if s == '':
                    if current_scanner:
                        # sort current scanner after all beacons have been read at this point
                        for b in scanners[current_scanner]:
                            b.set_neighbours(scanners[current_scanner])
                    # new scanner
                    continue
                else:
                    current_scanner = int(s.split()[-2])
            else:
                scanners[current_scanner].append(Beacon([int(d) for d in row]))
        print(scanners)

        for a, b in combinations(scanners.keys(), 2):
            print(f"scanner {a} with {len(scanners[a])} beacons and scanner {b} with {len(scanners[b])} beacons")
            count = 0
            for b1 in scanners[a]:
                print(f"{b1} from {a}...")
                for b2 in scanners[b]:
                    print(f"  with {b2}: ",end='')
                    if b1.intersection_count(b2) >= 1:
                        print("MATCH")
                        count += 1
                    else:
                        print("MISS")
            print(count)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = True
    PART2 = False
    SPLIT_LINES = True
    SPLIT_CHAR = ','

    with open(f'{script}{"-identical" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())

