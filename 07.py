import math
import os
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        numbers = [int(n) for n in data.split(',')]
        a = min(numbers)
        b = max(numbers)
        result = None
        cache = {}

        for i in range(a, b + 1):
            s = 0
            for n in numbers:
                d = abs(n - i)
                if modified:
                    if not d in cache:
                        cache[d] = d * (d + 1) >> 1  # Gauss
                    s += cache[d]
                else:
                    s += d
            if result is None or s < result:
                result = s

        return result


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    result = s.solve('16,1,2,0,4,2,7,1,2,14', True)
    print(result)
    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip())
    #     print(result)
    #
    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip(), True)
        print(result)
