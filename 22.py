import collections
import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}

Point3d = collections.namedtuple('Point3d', 'x, y, z', defaults=(0, 0, 0))


class Cuboid:
    def __init__(self, start: Point3d, end: Point3d):  # (x,y,) width (x->) height (->y) and depth (->z)
        self.start = start
        self.end = end

    def is_valid(self):
        return self.start.x < self.end.x and self.start.y < self.end.y and self.start.z < self.end.z

    def includes(self, other):
        return self.start.x <= other.start.x and self.end.x >= other.end.x and self.start.y <= other.start.y and self.end.y >= other.end.y and self.start.z <= other.start.z and self.end.z >= other.end.z

    def intersects(self, other):
        ix = (max(self.start.x, other.start.x), min(self.end.x, other.end.x))
        iy = (max(self.start.y, other.start.y), min(self.end.y, other.end.y))
        iz = (max(self.start.z, other.start.z), min(self.end.z, other.end.z))

        if ix[1] < ix[0] or iy[1] < iy[0] or iz[1] < iz[0]:
            return False  # no intersection
        return True

    def intersection(self, other):
        ix = (max(self.start.x, other.start.x), min(self.end.x, other.end.x))
        iy = (max(self.start.y, other.start.y), min(self.end.y, other.end.y))
        iz = (max(self.start.z, other.start.z), min(self.end.z, other.end.z))

        if ix[1] < ix[0] or iy[1] < iy[0] or iz[1] < iz[0]:
            return None  # no intersection

        return Cuboid(Point3d(ix[0], iy[0], iz[0]), Point3d(ix[1], iy[1], iz[1]))


    def cut(self, other):
        myself = None
        subcubes = []
        if other.start.x in range(self.start.x + 1, self.end.x + 1):  # other x somewhere within this cube?
            myself = Cuboid(self.start, Point3d(other.start.x - 1, self.end.y, self.end.z))
            subcubes.append(Cuboid(Point3d(other.start.x, self.start.y, self.start.z), self.end))
        if other.end.x in range(self.start.x, self.end.x):
            myself = Cuboid(Point3d(other.end.x + 1, self.start.y, self.start.z), self.end)
            subcubes.append(Cuboid(self.start, Point3d(other.end.x, self.end.y, self.end.z)))
            break

        if other.start.y in range(self.start.y + 1, self.end.y + 1):
            myself = Cuboid(self.start, Point3d(self.end.x, other.start.y - 1, self.end.z))
            subcubes.append(Cuboid(Point3d(self.start.x, other.start.y, self.start.z), self.end))
            break

        if other.end.y in range(self.start.y, self.end.y):
            myself = Cuboid(Point3d(self.start.x, other.end.y + 1, self.start.z), self.end)
            subcubes.append(Cuboid(self.start, Point3d(self.end.x, other.end.y, self.end.z)))
            break

        if other.start.z in range(self.start.z + 1, self.end.z + 1):
            myself = Cuboid(self.start, Point3d(self.end.x, self.end.y, other.start.z - 1))
            subcubes.append(Cuboid(Point3d(self.start.x, self.start.y, other.start.z), self.end))
            break

        if other.end.z in range(self.start.z, self.end.z):
            myself = Cuboid(Point3d(self.start.x, self.start.y, other.end.z + 1), self.end)
            subcubes.append(Cuboid(self.start, Point3d(self.end.x, self.end.y, other.end.z)))
            break

    def __str__(self):
        return f"[ {self.start} -- {self.end} ]"


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        # on x=10..12,y=10..12,z=10..12
        c1 = Cuboid(Point3d(10, 10, 10), Point3d(12, 12, 12))
        c2 = Cuboid(Point3d(11, 11, 11), Point3d(13, 13, 13))
        print(c1)
        print(c2)
        print(c1.cut(c2))

        cubes = []
        subcubes = []
        while True:
            for i in reversed(len(cubes)):
                other = cubes[i]



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = True
    SPLIT_LINES = True
    SPLIT_CHAR = False

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        s.solve()
