import os
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        chars = [defaultdict(int) for i in range(len(data[0]))]
        result = []

        for row in data:
            for i, c in enumerate(row):
                chars[i][c] += 1

        for letter_count in chars:
            # print(letter_count)
            c = None
            for k, v in letter_count.items():
                #print(k, v)
                if c is None or (modified and v < c[0]) or (not modified and v > c[0]):
                    c = (v, k)
            result.append(c[1])

        return int(''.join(result),2)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        upper = s.solve(f.read().strip().splitlines())
    with open(f'{script}-dev.txt') as f:
        lower = s.solve(f.read().strip().splitlines(), True)
    print(upper, lower, upper*lower)

    with open(f'{script}.txt') as f:
        upper = s.solve(f.read().strip().splitlines())
    with open(f'{script}.txt') as f:
        lower = s.solve(f.read().strip().splitlines(), True)

    print(upper, lower, upper * lower)
