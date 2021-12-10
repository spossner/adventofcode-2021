import os
import sys
from collections import defaultdict, deque

BRACES = {
    ')': '(',
    ']': '[',
    '>': '<',
    '}': '{',
}

SCORES = {
')': 3,
']': 57,
'}': 1197,
'>': 25137,
}

class Solution:
    def solve(self, data, modified=False):
        if not data:
            return None

        if type(data) is not list:
            data = [data]

        opening_braces = set(BRACES.values())

        score = 0
        for row in data:
            print(f"checking {row}")
            stack = deque()
            for c in row:

                if c in opening_braces:
                    stack.append(c)
                elif c in BRACES:
                    matching = stack.pop()
                    if BRACES[c] != matching:
                        score += SCORES[c]
                        break # stop with that row
                else:
                    print(f"unexpected char {c}")

        return score


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)
