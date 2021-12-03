import os
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        width = len(data[0])
        pos = 0
        while len(data) > 1 and pos < width:
            zeros = []
            ones = []
            for row in data:
                if row[pos] == '0':
                    zeros.append(row)
                else:
                    ones.append(row)

            if len(ones) >= len(zeros):
                data = zeros if modified else ones # use the desired rows
            else:
                data = ones if modified else zeros # use the desired rows

            if len(data) == 1: # found the number
                return int(data[0], 2)
            pos += 1 # next position

        return None



if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    script = '03'
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
