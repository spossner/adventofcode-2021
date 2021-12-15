import os
import sys
from collections import defaultdict, deque, Counter

OFFSETS = {
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1,)
}


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        self.rules = dict(line.split(" -> ") for line in data[2:])
        self.data = data[0]

        return self.buildPolymer(40) if modified else self.buildPolymer(10)

    def buildPolymer(self, iterations):
        freq = Counter([a + b for a, b in list(zip(self.data, self.data[1:]))])
        for _ in range(iterations):
            freq = sum([Counter({p[0] + self.rules[p]: freq[p], self.rules[p] + p[1]: freq[p]}) for p in freq], Counter())
        freq = (Counter({self.data[-1]: 1}) + sum([Counter({p[0]: freq[p]}) for p in freq], Counter())).most_common()
        return freq[0][1] - freq[-1][1]


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), True)
        print(result)
