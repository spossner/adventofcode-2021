import os
import sys
from collections import defaultdict

SEGMENTS = {
    1: 'cf',
    7: 'acf',
    4: 'bcdf',

    2: 'acdeg',
    3: 'acdfg',
    5: 'abdfg',

    0: 'abcefg',
    6: 'abdefg',
    9: 'abcdfg',

    8: 'abcdefg',
}

cipher = {
    "cf": 1,
    "acf": 7,
    "bcdf": 4,
    "acdeg": 2,
    "acdfg": 3,
    "abdfg": 5,
    "abcefg": 0,
    "abdefg": 6,
    "abcdfg": 9,
    "abcdefg": 8,
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

    def set_candidate(self, candidates, mappings, candidate_set):
        for no in mappings:
            candidates[no] = candidates[no].intersection(candidate_set)
        for no in set('abcdefg') - set(mappings):
            candidates[no] = candidates[no] - candidate_set

    def solve3(self, data, modified=False):
        if type(data) is not list:
            data = [data]

        sum_all = 0

        for line in data:
            patterns, digits = line.strip().split("|")
            right = digits
            patterns = sorted((set(dig) for dig in patterns.strip().split(" ")), key=len)
            digits = [set(dig) for dig in digits.strip().split(" ")]

            set_cf, set_acf, set_bcdf = patterns[:3]
            set_a = set_acf - set_cf
            set_bd = set_bcdf - set_acf
            for i in range(3, 9):
                patterns[i] -= set_a
            set_g = set.intersection(*patterns[3:9])
            for i in range(3, 9):
                patterns[i] -= set_g
            set_d = set.intersection(*patterns[3:6])
            set_b = set_bd - set_d
            set_cef = set.union(*patterns[3:6]) - set_b - set_d
            set_e = set_cef - set_bcdf
            for i in range(6, 9):
                patterns[i] = patterns[i] - set_b - set_d - set_e
            set_f = set.intersection(*patterns[6:9])
            set_c = set_cf - set_f

            transm = {
                tuple(*set_a)[0]: "a",
                tuple(*set_b)[0]: "b",
                tuple(*set_c)[0]: "c",
                tuple(*set_d)[0]: "d",
                tuple(*set_e)[0]: "e",
                tuple(*set_f)[0]: "f",
                tuple(*set_g)[0]: "g",
            }

            num = int(
                "".join(
                    str(cipher["".join(sorted(transm[d] for d in ds))]) for ds in digits
                )
            )
            print(f"{right}: {num}")
            sum_all += num

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

    # with open(f'{script}-dev.txt') as f:
    #    result = s.solve3(f.read().strip().splitlines(), True)
    #    print(result)
    #
    with open(f'{script}.txt') as f:
        result = s.solve3(f.read().strip().splitlines(), True)
        print(result)


