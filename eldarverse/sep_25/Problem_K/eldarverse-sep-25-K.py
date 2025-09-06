"""Eldarverse Puzzles - Problem K
Solution Started: September 6,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-K
Solution by: Abbas Moosajee
Brief: [Electrical Outlets]"""

#!/usr/bin/env python3
from pathlib import Path
import math
from itertools import combinations, permutations

# Load input file
input_file = "problem-sep-25-long-K-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()


def parse_raw_data(raw_data):
    parsed_data = []
    new_test = True
    line_no = 0
    while line_no < len(raw_data) - 1:
        line_no += 1
        line_data = tuple(map(int, raw_data[line_no].split()))
        if new_test:
            laptops, sockets = [], []
            N, K = line_data
            line_no += 1
            cables = tuple(map(int, raw_data[line_no].split()))
            add_laptops = N + line_no
            add_sockets = K + N + line_no
            new_test = False
        elif line_no <= add_laptops:
            laptops.append(line_data)
        elif line_no <= add_sockets:
            sockets.append(line_data)
            if line_no == add_sockets:
                new_test = True
                if len(laptops) != N and len(sockets) != K:
                    raise ValueError("Missed some data")
                parsed_data.append([cables, laptops, sockets])
    return parsed_data

class CableManager:
    def __init__(self, laptops, sockets):
        self.laptops = laptops
        self.sockets = sockets

    @staticmethod
    def _calc_distance_sq(pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return dx*dx + dy*dy

    @staticmethod
    def _min_cable_for_distance_sq(d2: int) -> int:
        r = math.isqrt(d2)
        return r if r*r == d2 else r+1

    def arrange_cables(self, cables):
        N = len(self.laptops)
        K = len(self.sockets)
        cables_sorted = sorted(cables, reverse=True)
        max_possible = min(N, K)

        # precompute distances
        dist2 = {}
        for i, l in enumerate(self.laptops):
            for j, s in enumerate(self.sockets):
                dist2[(i, j)] = self._calc_distance_sq(l, s)

        # search for largest r feasible
        for r in range(max_possible, -1, -1):
            for laptop_subset in combinations(range(N), r):
                for socket_subset in combinations(range(K), r):
                    for socket_perm in permutations(socket_subset, r):
                        required = []
                        for li, sj in zip(laptop_subset, socket_perm):
                            L = self._min_cable_for_distance_sq(dist2[(li, sj)])
                            required.append(L)
                        required.sort(reverse=True)
                        if len(cables_sorted) < r:
                            continue
                        candidate_cables = cables_sorted[:r]
                        feasible = all(c >= need for c, need in zip(candidate_cables, required))
                        if feasible:
                            return N - r
        return N  # if nothing matched


test_cases = parse_raw_data(data)
solutions =  []
for case_no, case_data in enumerate(test_cases[:], start = 1):
    cables, laptops, sockets = case_data
    room_setup = CableManager(laptops, sockets)
    powerless = room_setup.arrange_cables(cables)
    solutions.append(f"Case #{case_no}: {powerless}")
    print(solutions[-1])

output_file = "problem-sep-25-long-K-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))

