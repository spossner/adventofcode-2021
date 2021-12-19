from __future__ import nested_scopes

import operator
import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

DIRECT_ADJACENTS = ((0, -1), (-1, 0), (1, 0), (0, 1))  # 4 adjacent nodes
ALL_ADJACENTS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
HEX_ADJACENTS = ((1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1))


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        homework = [SnailfishNumber.parse(task) for task in self.data]
        print(f"Part 1: {reduce(add, homework).magnitude()}")
        print(
            f"Part 2: {max(add(SnailfishNumber.parse(a), SnailfishNumber.parse(b)).magnitude() for a in self.data for b in self.data if a != b)}")


class SnailfishNumber:  # pure int value or pair of left and right
    def __init__(self, value=None, left=None, right=None):
        if value is not None:
            assert type(value) != SnailfishNumber
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.left},{self.right}]"

    def flatlist(self, vs):
        if self.value is not None:
            vs.append(self)
        if self.left:
            self.left.flatlist(vs)
        if self.right:
            self.right.flatlist(vs)
        return vs

    def replace(self, a, b):
        if self.left == a:
            self.left = b
        else:
            self.right = b

    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @classmethod
    def __parsefish(cls, s, i=0):
        if s[i].isdigit():
            return SnailfishNumber(int(s[i])), i + 1
        f = SnailfishNumber()
        f.left, i = cls.__parsefish(s, i + 1)
        f.right, i = cls.__parsefish(s, i + 1)
        return f, i + 1

    @classmethod
    def parse(cls, s):
        return cls.__parsefish(s)[0]


def explode(f, vs, d=0, p=None):
    if f.value is not None:
        return False
    if d == 4:
        i = vs.index(f.left)
        if i > 0:
            vs[i - 1].value += f.left.value
        if i < len(vs) - 2:
            vs[i + 2].value += f.right.value
        p.replace(f, SnailfishNumber(0))
        return True
    if explode(f.left, vs, d + 1, f):
        return True
    return explode(f.right, vs, d + 1, f)


def split(f, d=0, p=None):
    if f.value is not None:
        if f.value < 10:
            return False
        p.replace(f, SnailfishNumber(left=SnailfishNumber(f.value >> 1), right=SnailfishNumber(f.value - (f.value >> 1))))
        return True
    if split(f.left, d + 1, f):
        return True
    return split(f.right, d + 1, f)


def add(a, b):
    f = SnailfishNumber(left=a, right=b)
    while True:
        if not explode(f, f.flatlist([])):
            if not split(f):
                break
    return f


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    SPLIT_LINES = True
    SPLIT_CHAR = None

    # with open(f'{script}-explodes.txt') as f:
    #     for row in f.read().strip().splitlines():
    #         n = SnailfishNumber.parse(row)
    #         print(n, end=' -> ')
    #         if explode(n, n.flatlist([])):
    #             print(n)
    #         else:
    #             print("NOTHING TO DO")

    # a = SnailfishNumber.parse('[[[[4,3],4],4],[7,[[8,4],9]]]')
    # b = SnailfishNumber.parse('[1,1]')
    # result = add(a, b)
    # print(result)


#     data = [SnailfishNumber.parse(s) for s in '''[1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# [6,6]'''.splitlines()]
#     print(reduce(add, data))

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
