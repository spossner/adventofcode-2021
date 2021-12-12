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

        paths = defaultdict(list)
        for row in data:
            name, next = row.split('-')
            paths[name].append(next)
            paths[next].append(name)
        print(paths)

        d = deque()
        d.append(('start', ['start'], [], ''))  # name, path, seen, twice
        # results = []
        result = 0
        while d:
            for _ in range(len(d)):
                node, path, seen, twice = d.popleft()
                if node == 'end':
                    #results.append(path)
                    result += 1
                    continue

                if node.islower():
                    if node in seen: # visit lower case cave twice
                        if node not in ('start','end') and twice == '':
                            twice = node
                        else:
                            continue
                    else:
                        seen = [*seen, node]

                for nxt in paths[node]:
                    d.append((nxt, [*path, nxt], seen, twice))

        return result


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
