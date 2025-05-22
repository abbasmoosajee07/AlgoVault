"""Codyssi Puzzles - Problem 18
Solution Started: May 17, 2025
Puzzle Link: https://www.codyssi.com/view_problem_22?
Solution by: Abbas Moosajee
Brief: [Cataclysmic Escape]
"""

#!/usr/bin/env python3

import os, re, copy, time, heapq
from itertools import product
from math import gcd
from functools import reduce
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input3.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

class Submarine:
    MAX_HEALTH = 3

    def __init__(self, input_data, dimensions, target):
        self.dimensions, self.target_coords = dimensions, target
        self.setup_dimensions()
        self.data = input_data
        self.parse_debris_data()

    def lcm(self, *args):
        def lcm_pair(a, b):
            return a * b // gcd(a, b)
        return reduce(lcm_pair, args)

    def setup_dimensions(self):
        self.dim_x, self.dim_y, self.dim_z, self.dim_a = self.dimensions
        self.dim_xyza = self.dim_x * self.dim_y * self.dim_z * self.dim_a
        self.dim_yza = self.dim_y * self.dim_z * self.dim_a
        self.dim_za = self.dim_z * self.dim_a
        self.debris_cycle = self.lcm(self.dim_x, self.dim_y, self.dim_z, self.dim_a)

    def idx(self, x, y, z, a):
        return x * self.dim_yza + y * self.dim_za + z * self.dim_a + a + 1

    def idxr(self, pos):
        x, rem = divmod(pos, self.dim_yza)
        y, rem = divmod(rem, self.dim_za)
        z, rem = divmod(rem, self.dim_a)
        a = rem - 1
        return x, y, z, a

    def parse_debris_data(self):
        self.debris = [[0] * self.dim_xyza for _ in range(self.debris_cycle)]

        for line in self.data:
            s = line.split()
            fx, fy, fz, fa = [int(term[:-1]) for term in s[2].split("+")]
            d = int(s[4])
            r = int(s[7])
            vx, vy, vz, va = [int(v.strip('(),')) for v in s[11:15]]

            for pos in range(self.dim_xyza):
                x, y, z, a = self.idxr(pos)
                if (fx * x + fy * y + fz * z + fa * a) % d == r:
                    self.update_debris_path(x, y, z, a, vx, vy, vz, va)

    def update_debris_path(self, x, y, z, a, vx, vy, vz, va):
        for t in range(self.debris_cycle):
            self.debris[t][self.idx(x, y, z, a)] += 1
            x = (x + vx) % self.dimensions[0]
            y = (y + vy) % self.dimensions[1]
            z = (z + vz) % self.dimensions[2]
            a = (a + va + 1) % self.dimensions[3] - 1

    def count_debris(self):
        return sum(self.debris[0])

    def acceptable_path(self):
        start = self.idx(0, 0, 0, 0)
        target = self.idx(*self.target_coords)

        hits = [self.MAX_HEALTH + 1] * self.dim_xyza
        hits[start] = 0
        t = 0

        while hits[target] > self.MAX_HEALTH:
            t += 1
            hits_new = hits[:]
            for pos, count in enumerate(hits):
                if count > self.MAX_HEALTH:
                    continue
                x, y, z, a = self.idxr(pos)
                for nx, ny, nz, na in self.try_neighbors(x, y, z, a):
                    new_pos = self.idx(nx, ny, nz, na)
                    hits_new[new_pos] = min(hits_new[new_pos], count)
            for pos, count in enumerate(self.debris[t % self.debris_cycle]):
                hits_new[pos] += count
            hits_new[start] = 0
            hits = hits_new

        return t

    def safe_flight(self):
        start = self.idx(0, 0, 0, 0)
        target = self.idx(*self.target_coords)

        safe = [False] * self.dim_xyza
        safe[start] = True
        t = 0

        while not safe[target]:
            t += 1
            safe_new = safe[:]
            for pos, ok in enumerate(safe):
                if not ok:
                    continue
                x, y, z, a = self.idxr(pos)
                for nx, ny, nz, na in self.try_neighbors(x, y, z, a):
                    new_pos = self.idx(nx, ny, nz, na)

                    safe_new[new_pos] = True
            for pos, count in enumerate(self.debris[t % self.debris_cycle]):
                if count > 0:
                    safe_new[pos] = False
            safe_new[start] = True
            safe = safe_new

        return t

    def try_neighbors(self, x, y, z, a):
        deltas = [(1, 0, 0), (-1, 0, 0),
                    (0, 1, 0), (0, -1, 0),
                    (0, 0, 1), (0, 0, -1)]
        neighbors = []
        for dx, dy, dz in deltas:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < self.dimensions[0] and 0 <= ny < self.dimensions[1] and 0 <= nz < self.dimensions[2]:
                neighbors.append((nx, ny, nz, a))
        return neighbors

feasible, target_coords = ((10, 15, 60, 3), (9, 14, 59, 0))
sub = Submarine(input_data, feasible, target_coords)

debris = sub.count_debris()
print("Part 1:", debris)

safest_path = sub.safe_flight()
print("Part 2:", safest_path)

acceptable_path = sub.acceptable_path()
print("Part 3:", acceptable_path)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
