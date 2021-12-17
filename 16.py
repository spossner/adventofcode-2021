import os
import sys
import uuid
from collections import deque
from functools import total_ordering, reduce
import bisect
from random import random

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}

BITS = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

class Solution:
    def solve(self, data, modified=False):
        bits = list(''.join([BITS[c] for c in data]))
        packets = []
        n = self.parse(bits, packets, True)
        if modified:
            return n[1][0]
        print(packets)
        return packets
        # result = 0
        # for p in packets:
        #     result += p[1]
        # return result

    def parse(self, bits, packets=[], outer=False, max_packets=None, indent=0):
        ptr = 0
        packets_found = 0
        new_packets = []
        while ptr < len(bits):
            if ptr >= len(bits)-6:
                if outer:
                    break
                print(f"{' ' * indent}[{block}] not enough bits left {ptr}, {len(bits)}: {bits[ptr:]}")
            version = ''.join(bits[ptr:ptr+3])
            id = ''.join(bits[ptr+3:ptr+6])
            packets.append((ptr, int(version,2), id)) # start, version, id
            block = str(uuid.uuid4()).split('-')[-1]
            print(f"{' ' * indent}[{block}] {ptr}: {version}:{id} in {''.join(bits[ptr:ptr+20])}...")
            ptr += 6
            if id == '100': # literal
                print(f"{' ' * (indent+2)}[{block}] parsing literal", end='')
                number = []
                reading = True
                while reading:
                    print('.', end='')
                    block = bits[ptr:ptr + 5]
                    if block[0] == '0':
                        reading = False
                    number.extend(bits[ptr+1:ptr+5]) # add the 4 bits
                    ptr += 5
                print(f" -> {int(''.join(number), 2)}")
                new_packets.append(int(''.join(number), 2))
            else:
                mode = bits[ptr]
                ptr += 1
                found = None
                if mode == '0':
                    length_bits = bits[ptr:ptr+15]
                    ptr += 15
                    length = int(''.join(length_bits),2)
                    consumed, found = self.parse(bits[ptr:ptr+length], packets, False, None, indent+2)
                    assert consumed == length
                    ptr += length
                else:
                    length_bits = bits[ptr:ptr + 11]
                    ptr += 11
                    length = int(''.join(length_bits), 2)
                    consumed, found = self.parse(bits[ptr:], packets, False, length, indent+2)
                    ptr += consumed
                # process found
                print(f"{' ' * indent}[{block}] {ptr}: {version}:{id} consumed {consumed} => {found}")
                if id == '000':
                    new_packets.append(sum(found))
                elif id == '001':
                    result = 1
                    for d in found:
                        result *= d
                    new_packets.append(result)
                elif id == '010':
                    new_packets.append(min(found))
                elif id == '011':
                    new_packets.append(max(found))
                elif id == '101':
                    new_packets.append(1 if found[0] > found[1] else 0)
                elif id == '110':
                    new_packets.append(1 if found[0] < found[1] else 0)
                elif id == '111':
                    new_packets.append(1 if found[0] == found[1] else 0)

            if outer or max_packets is not None and len(new_packets) >= max_packets:
                break
        return (ptr, new_packets)

if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]
    print(f"STARTING {script}")

    part2 = True

    s = Solution()
    with open(f'{script}-dev.txt') as f:
        if not part2:
            print(s.solve('D2FE28', part2))
            print(s.solve('38006f45291200', part2))
            print(s.solve('EE00D40C823060', part2))
            assert reduce(lambda acc, b: acc + b[1], s.solve('8A004A801A8002F478', part2), 0) == 16
            assert reduce(lambda acc, b: acc + b[1], s.solve('620080001611562C8802118E34', part2), 0) == 12
            assert reduce(lambda acc, b: acc + b[1], s.solve('C0015000016115A2E0802F182340', part2), 0) == 23
            assert reduce(lambda acc, b: acc + b[1], s.solve('A0016C880162017C3686B18A3D4780', part2), 0) == 31

        if part2:
            assert s.solve('C200B40A82', part2) == 3
            assert s.solve('04005AC33890', part2) == 54
            assert s.solve('880086C3E88112', part2) == 7
            assert s.solve('CE00C43D881120', part2) == 9
            assert s.solve('D8005AC2A8F0', part2) == 1
            assert s.solve('F600BC2D8F', part2) == 0
            assert s.solve('9C005AC2F8F0', part2) == 0
            assert s.solve('9C0141080250320F1802104A08', part2) == 1

    with open(f'{script}.txt') as f:
        result = s.solve(f.read().strip(), part2)
        print(result)
        # 99295798 is wrong... too low
        # did not break out of loop after reading enough packets from operator path of the method...
        # 19348959966392