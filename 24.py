import os
import random
import sys
from collections import defaultdict, deque


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self, nr=None):
        inp = deque(str(nr)) if nr is not None else None
        ptr = 0
        count = 0
        self.registers = defaultdict(int)
        while ptr < len(self.data):
            count += 1
            instr = self.data[ptr]

            cmd = instr[0]
            if cmd == 'nop':
                pass
            elif cmd == 'inp':
                self.registers[instr[1]] = int(inp.popleft()) if inp is not None else int(input(f"{instr[1]}: "))
            elif cmd == 'add':
                try:
                    self.registers[instr[1]] += int(instr[2])
                except ValueError:
                    self.registers[instr[1]] += self.registers[instr[2]]
            elif cmd == 'mul':
                try:
                    self.registers[instr[1]] = self.registers[instr[1]] * int(instr[2])
                except ValueError:
                    self.registers[instr[1]] = self.registers[instr[1]] * self.registers[instr[2]]
            elif cmd == 'div':
                try:
                    self.registers[instr[1]] = int(self.registers[instr[1]] / int(instr[2]))
                except ValueError:
                    self.registers[instr[1]] = int(self.registers[instr[1]] * self.registers[instr[2]])
            elif cmd == 'mod':
                try:
                    self.registers[instr[1]] = self.registers[instr[1]] % int(instr[2])
                except ValueError:
                    self.registers[instr[1]] = self.registers[instr[1]] % self.registers[instr[2]]
            elif cmd == 'eql':
                try:
                    self.registers[instr[1]] = 1 if self.registers[instr[1]] == int(instr[2]) else 0
                except ValueError:
                    self.registers[instr[1]] = 1 if self.registers[instr[1]] == self.registers[instr[2]] else 0
            else:
                raise SyntaxError(f'unexpected command {instr} at line {ptr}')
            ptr += 1
        return self.registers

    def reset(self):
        pass


def model_numbers():
    for i in range(99999999999999, 11111111111110, -1):
        nr = str(i)
        if '0' in nr:
            continue
        yield i


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    SPLIT_LINES = True
    SPLIT_CHAR = ' '


    # with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
    #     s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
    #     count = 0
    #     for i in model_numbers():
    #         if count % 10000 == 0:
    #             print(i)
    #         count += 1
    #         s.solve(i)
    #         if s.registers['z'] == 0:
    #             print(s.registers)
    #             break


    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        instr, stack = f.read().strip().splitlines(), []

        p, q = 99999999999999, 11111111111111

        for i in range(14):
            a = int(instr[18 * i + 5].split()[-1])
            b = int(instr[18 * i + 15].split()[-1])

            if a > 0: stack += [(i, b)]; continue
            j, b = stack.pop()

            p -= abs((a + b) * 10 ** (13 - [i, j][a > -b]))
            q += abs((a + b) * 10 ** (13 - [i, j][a < -b]))

        print(p, q)