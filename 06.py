import os
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, days=18):
        if type(data) is not list:
            data = [data]
        fishes = [0] * 9
        for i in data[0].split(','):
            fishes[int(i)] += 1
        print(f"Initial fish-states: {fishes}")
        for i in range(1, days+1):
            zero = fishes[0]
            fishes = [*fishes[1:], zero]
            fishes[6] += zero
            print(f"After {i:>2} days: {fishes}")

        return sum(fishes)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    #with open(f'{script}-dev.txt') as f:
    #    result = s.solve(f.read().strip().splitlines(), 256)
    #    print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines(), 256)
        print(result)


