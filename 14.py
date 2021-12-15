import os
import sys
from collections import defaultdict, deque

OFFSETS = {
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1,)
}


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        poly = list(data[0])
        chars = defaultdict(int)
        for p in poly:
            chars[p] += 1
        rules = {}
        for row in data[2:]:
            pattern, ins = row.split(' -> ')
            rules[pattern] = ins

        # check development of each rule for itself..
        rule = 'HH'
        print(f"CHECKING {rule}")
        chars = defaultdict(int) #
        poly = list(rule)
        for p in poly:
            chars[p] += 1

        for n in range(15):
            i = 0
            while i < len(poly) - 1:
                p = poly[i] + poly[i + 1]
                if p in rules:
                    poly.insert(i + 1, rules[p])
                    chars[rules[p]] += 1  # add one more
                    i += 2
                else:
                    i += 1
            print(n, len(poly), chars, ''.join(poly))
            pass

        return 0
        print(poly, rules)
        count = 0
        for n in range(40):
            i = 0
            while i < len(poly) - 1:
                p = poly[i] + poly[i + 1]
                if p in rules:
                    poly.insert(i + 1, rules[p])
                    chars[rules[p]] += 1 # add one more
                    i += 2
                else:
                    i += 1
            # print(f"After: {''.join(poly)}")
            print(f"{n}: {len(poly)}")
        print(len(poly))
        print(chars)
        return max(chars.values()) - min(chars.values())


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)

    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip().splitlines())
    #     print(result)
