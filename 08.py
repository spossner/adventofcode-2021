import os
import sys
from collections import defaultdict

SEGMENTS = {
    # special in 0-2
    'cf': '1',
    'acf': '7',
    'bcdf': '4',

    # 5 segments in 3-5
    'acdeg': '2',
    'acdfg': '3',
    'abdfg': '5',

    # 6 segments in 6-8
    'abcefg': '0',
    'abdefg': '6',
    'abcdfg': '9',

    # all 7 segments in 9
    'abcdefg': '8',
}

class Solution:
    def solve(self, data, modified=False):
        if type(data) is not list:
            data = [data]
        counts = [0] * 10

        for row in data:
            left, right = row.split('|')
            digits = right.strip().split(' ')
            for d in digits:
                counts[len(d)] += 1

        return sum((counts[2],counts[4],counts[3],counts[7]))

    def solve2(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        sum_all = 0

        for line in data:
            candidates, right = line.strip().split("|")
            candidates = sorted((set(n) for n in candidates.strip().split(" ")), key=len)
            digits = [set(n) for n in right.strip().split(" ")]

            candidates_cf, candidates_acf, candidates_bcdf = candidates[:3] # all samples contain the three numbers
            assert len(candidates_cf) == 2
            assert len(candidates_acf) == 3
            assert len(candidates_bcdf) == 4

            candidates_bd = candidates_bcdf - candidates_acf # 4 without 7 gives b and d candidates
            candidates_a = candidates_acf - candidates_cf # 7 without the 1..
            for i in range(3, 9):
                candidates[i] = candidates[i] - candidates_a

            # all 5/6 had a and g together -> w/a juts g left
            candidates_g = set.intersection(*candidates[3:9])
            for i in range(3, 9):
                candidates[i] = candidates[i] - candidates_g

            # d left in 5 segments digits
            candidates_d = set.intersection(*candidates[3:6])
            candidates_b = candidates_bd - candidates_d
            # all the rest from the 5 segments w/o b and d
            candidates_cef = set.union(*candidates[3:6]) - candidates_b - candidates_d
            candidates_e = candidates_cef - candidates_bcdf
            for i in range(6, 9):
                candidates[i] = candidates[i] - candidates_b - candidates_d - candidates_e
            candidates_f = set.intersection(*candidates[6:9])
            candidates_c = candidates_cf - candidates_f

            mapping = {
                list(candidates_a)[0]: "a",
                list(candidates_b)[0]: "b",
                list(candidates_c)[0]: "c",
                list(candidates_d)[0]: "d",
                list(candidates_e)[0]: "e",
                list(candidates_f)[0]: "f",
                list(candidates_g)[0]: "g",
            }

            result = [SEGMENTS["".join(sorted(mapping[d] for d in digit))] for digit in digits]
            print(f"{right}: {result}")
            sum_all += int("".join(result))

        return sum_all


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")
    s = Solution()

    # with open(f'{script}-dev.txt') as f:
    #    result = s.solve(f.read().strip().splitlines())
    #    print(result)

    # with open(f'{script}.txt') as f:
    #     result = s.solve(f.read().strip().splitlines())
    #     print(result)

    # print(s.solve3('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'))

    with open(f'{script}-dev.txt') as f:
       result = s.solve2(f.read().strip().splitlines(), True)
       print(result)
    #
    with open(f'{script}.txt') as f:
        result = s.solve2(f.read().strip().splitlines(), True)
        print(result)


