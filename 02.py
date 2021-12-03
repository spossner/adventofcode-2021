class Solution:
    def solve(self, data):
        if type(data) is not list:
            data = [data]
        data = [(cmd[0], int(distance)) for cmd, distance in (row.split(' ') for row in data)]
        print(data)
        pos = (0, 0)
        depth = 0
        for cmd, distance in data:
            if cmd == 'f':
                pos = (pos[0]+distance, pos[1])
            elif cmd == 'd':
                depth += distance
            elif cmd == 'u':
                depth -= distance

        print(pos, depth)
        return pos[0] * depth

    def solve2(self, data):
        if type(data) is not list:
            data = [data]
        data = [(cmd[0], int(distance)) for cmd, distance in (row.split(' ') for row in data)]
        print(data)
        pos = 0
        depth = 0
        aim = 0
        for cmd, distance in data:
            if cmd == 'f':
                pos += distance
                depth += aim * distance
            elif cmd == 'd':
                aim += distance
            elif cmd == 'u':
                aim -= distance

        print(pos, depth, aim)
        return pos * depth

if __name__ == '__main__':
    s = Solution()
    #with open('02-dev.txt') as f:
    #    print(s.solve(f.read().strip().splitlines()))
    #with open('02.txt') as f:
    #    print(s.solve(f.read().strip().splitlines()))

    print("PART 2")
    with open('02-dev.txt') as f:
        print(s.solve2(f.read().strip().splitlines()))
    with open('02.txt') as f:
        print(s.solve2(f.read().strip().splitlines()))
