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
        winners = []
        while start < len(data):
            card = [[0] * 6 for i in range(6)] # extra row and extra column
            for y in range(5):
                card[y] = [int(a) for a in data[start+y].split()]
                card[y].append(0)
            cards.append(card)
            start = start + 6 # skip empty line

        print(numbers)
        print(cards)

        for n in numbers:
            for id, card in enumerate(cards):
                if id in winners:
                    continue
                for row in card[:-1]:
                    try:
                        i = row[:-1].index(n)
                        row[i] = (n, True) # mark cell and make it not found by subsequent searches
                        row[-1] += 1
                        card[-1][i] += 1
                        if row[-1] == 5 or card[-1][i] == 5:
                            winners.append(id)
                            if not modified or len(winners) == len(cards):
                                return (n, [row[:-1] for row in card[:-1]]) # found winner
                    except ValueError:
                        pass

        return None


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    s = Solution()

    with open(f'{script}.txt') as f:
        n, card = s.solve(f.read().strip().splitlines(), True)
        sum = 0
        print(n, card)
        for row in card:
            for v in row:
                sum = sum + (v if type(v) == int else 0)
        print(sum*n)


