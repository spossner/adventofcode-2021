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
'(': 1,
'[': 2,
'{': 3,
'<': 4,
}

class Solution:
    def solve(self, data, modified=False):
        if not data:
            return None

        if type(data) is not list:
            data = [data]

        opening_braces = set(BRACES.values())

        incomplete = []
        for row in data:
            print(f"checking {row}")
            stack = deque()
            valid = True
            for c in row:
                if c in opening_braces:
                    stack.append(c)
                elif c in BRACES:
                    if not stack:
                        valid = False
                        break
                    matching = stack.pop()
                    if BRACES[c] != matching:
                        print(f"{matching} does not match {c}")
                        valid = False
                        break # stop with that row
                else:
                    print(f"unexpected char {c}")
            if valid and stack:
                print(f"found incomplete {row}")
                incomplete.append(stack)
        print(incomplete)
        scores = []
        for missing in incomplete:
            score = 0
            for c in reversed(missing):
                score = score * 5 + SCORES[c]
            scores.append(score)
        scores.sort()
        return scores[len(scores)>>1]


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
