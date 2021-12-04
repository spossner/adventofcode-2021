import os
import sys
from collections import defaultdict


class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        numbers = [int(a) for a in data[0].split(',')]
        cards = []
        start = 2
        while start < len(data):
            card = [[0] * 5 for i in range(5)]
            for y in range(5):
                card[y] = [int(a) for a in data[start+y].split()]
            cards.append(card)
            start = start + 6 # skip empty line

        print(numbers)
        print(cards)

        for n in numbers:
            for card in cards:
                for row in card:
                    i = row.index(n)




if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    with open(f'{script}-dev.txt') as f:
        result = s.solve(f.read().strip().splitlines())
        print(result)


