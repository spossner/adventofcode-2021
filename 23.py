import collections
import heapq
import os
import sys
from collections import deque, defaultdict
from functools import total_ordering, reduce
import bisect
from itertools import permutations

DIRECT_ADJACENTS = {(0, -1), (-1, 0), (1, 0), (0, 1), }  # 4 adjacent nodes
ALL_ADJACENTS = {(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1,)}

MOVE_COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

HALL_LEN = 11

ROOMS_AT = [(2, "A"), (4, "B"), (6, "C"), (8, "D")]
ROOMS = len(ROOMS_AT)
NO_STOP = set([pos for (pos, pod) in ROOMS_AT])
WANT_ROOM = {"A": 0, "B": 1, "C": 2, "D": 3}


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self):
        rooms = [[c for c in l.strip()] for l in self.data]
        if self.modified:
            # D#C#B#A#
            # D#B#A#C#
            for room, insert in zip(rooms, ['DD', 'CB', 'BA', 'AC']):
                room.insert(1, insert[0])
                room.insert(2, insert[1])
        print(rooms)

        start = State(hall=[None] * 11, rooms=rooms)
        visited = set()
        heap = [(0, start, ())]
        solutions = []
        while heap:
            cost, state, path = heapq.heappop(heap)
            if state in visited:
                continue

            print("cost", cost, "state", state)
            visited.add(state)

            if state.final():
                for st in path:
                    print(st)
                print("final", cost)
                return

            for move_cost, move_to_state in state.valid_moves():
                heapq.heappush(heap, (cost + move_cost, move_to_state, tuple(list(path) + [state])))


@total_ordering
class State(object):
    def __init__(self, hall, rooms):
        assert (len(hall) == HALL_LEN)
        assert (len(rooms) == ROOMS)
        self._room_len = len(rooms[0])
        assert (all([len(room) == self._room_len for room in rooms]))

        self._hall = tuple([c if c != '.' else None for c in hall])
        assert (all([not c or c in MOVE_COSTS for c in self._hall]))
        self._rooms = tuple([tuple([c if c != '.' else None for c in room]) for room in rooms])
        assert (all([all([not c or c in MOVE_COSTS for c in room]) for room in self._rooms]))

    def __repr__(self):
        hallstr = ''.join(['.' if not c else c for c in self._hall])
        roomstrs = tuple([''.join(['.' if not c else c for c in room]) for room in self._rooms])
        return f"State(hall='{hallstr}', rooms={roomstrs})"

    def __hash__(self):
        return hash((self._hall, self._rooms))

    def __eq__(self, other):
        return (self._hall, self._rooms) == (other._hall, other._rooms)

    def __lt__(self, other):
        return repr(self) < repr(other)

    def final(self):
        return all([room[0] == want and room[1] == want for (room, (ignored, want)) in zip(self._rooms, ROOMS_AT)])

    # Returns [ (cost, State), (cost, State), ... ] in ascending cost order.
    def valid_moves(self):
        # * Amphipods will never stop on the space immediately outside any room.
        # * Amphipods will never move from the hallway into a room unless that room is their destination room
        #   and that room contains no amphipods which do not also have that room as their own destination.
        # * Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.

        out = []

        # Compute moves for pods in the hall
        for i in range(HALL_LEN):
            out.extend(self._moves_from_hall(i))

        for i in range(ROOMS):
            out.extend(self._moves_from_room(i))

        return sorted(out)

    # Assuming a pod is standing right outside their wanted room, what
    # valid moves are there?
    #
    # Returns None or (cost, new rooms array).
    def _moves_into_wanted_room(self, pod):
        room_idx = WANT_ROOM[pod]
        room = self._rooms[room_idx]

        # First figure out if `pod` can even move in.
        if not all([not c or c == pod for c in room]):
            return None

        # Find the last empty slot
        for steps in range(self._room_len, 0, -1):
            if not room[steps - 1]:
                break

        # Create a new room array usable for State()
        rooms = [list(room[:]) for room in self._rooms]
        rooms[room_idx][steps - 1] = pod
        return (MOVE_COSTS[pod] * steps, tuple([tuple(room) for room in rooms]))

    # Returns any valid states starting from idx in hall, with costs
    def _moves_from_hall(self, idx):
        if not self._hall[idx]:
            # no pod here
            return []
        pod = self._hall[idx]
        pod_room_idx = ROOMS_AT[WANT_ROOM[pod]][0]
        for check_idx in between(idx, pod_room_idx):
            # Is there a pod in the way?
            if self._hall[check_idx]:
                return []
        # No pods in the way, check if we can get in.
        room_move = self._moves_into_wanted_room(pod)
        if not room_move:
            return []

        # We can move to pod to its room.
        cost, new_rooms = room_move
        cost += dist(idx, pod_room_idx) * MOVE_COSTS[pod]
        hall = list(self._hall[:])
        hall[idx] = None
        hall = tuple(hall)
        return [(cost, State(hall=hall, rooms=new_rooms))]

    def _moves_from_room_to_hall(self, room_idx):
        room_pos, pod_wanted = ROOMS_AT[room_idx]
        room = self._rooms[room_idx]

        if all([not c or c == pod_wanted for c in room]):
            # every space is either empty or already set
            return None

        for idx in range(self._room_len):
            if room[idx]:
                break

        rooms = [list(room[:]) for room in self._rooms]
        pod = rooms[room_idx][idx]
        rooms[room_idx][idx] = None
        return (MOVE_COSTS[pod] * (idx + 1), pod, room_pos, tuple([tuple(room) for room in rooms]))

    def _moves_from_room(self, room_idx):
        found = self._moves_from_room_to_hall(room_idx)
        if not found:
            return []

        cost, pod, room_pos, new_rooms = found
        # A pod can leave the room and is now at position `pos`.

        possible_stops = []
        for pos in between(room_pos, HALL_LEN):
            if self._hall[pos]:
                # There's a pod in the way.
                break
            possible_stops.append(pos)
        for pos in between(room_pos, -1):
            if self._hall[pos]:
                # There's a pod in the way.
                break
            possible_stops.append(pos)

        out = []
        for stop in possible_stops:
            if stop in NO_STOP:
                continue
            new_hall = list(self._hall[:])
            new_hall[stop] = pod
            new_hall = tuple(new_hall)
            out.append((cost + MOVE_COSTS[pod] * dist(room_pos, stop), State(hall=new_hall, rooms=new_rooms)))

        return out


def between(idx1, idx2):
    if idx1 < idx2:
        return range(idx1 + 1, idx2)
    return range(idx1 - 1, idx2, -1)


def dist(idx1, idx2):
    return abs(idx1 - idx2)


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = False
    PART2 = False
    SPLIT_LINES = True
    SPLIT_CHAR = False

#     s = Solution('''BA
# CD
# BC
# DA''', PART2, SPLIT_LINES, SPLIT_CHAR)
#     s.solve()

    s = Solution('''DB
DC
BA
AC''', True, SPLIT_LINES, SPLIT_CHAR)
    s.solve()
