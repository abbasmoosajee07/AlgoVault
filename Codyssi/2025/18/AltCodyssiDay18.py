"""Codyssi Puzzles - Problem 18
Solution Started: May 17, 2025
Puzzle Link: https://www.codyssi.com/view_problem_22?
Solution by: Abbas Moosajee
Brief: [Cataclysmic Escape]
"""

#!/usr/bin/env python3

import os, re, copy, time, heapq
from itertools import product
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')
    feasible_spaces = {
        "Day18_input1.txt":((10, 15, 60, 3), (9, 14, 59, 0)), "Day18_input2.txt":((3,3,5,3),(2, 2, 4, 0)),
        "Day18_input.txt": ((10, 15, 60, 3),(9, 14, 59, 0)), "Day18_input3.txt":((10, 15, 60, 3), (9, 14, 59, 0))}
    feasible, target_coords = feasible_spaces[D18_file]

class Submarine:
    def __init__(self, all_rules, feasible_space):
        MIN_LIMITS = (0, 0, 0, -1)
        self.idx_map = {"x": 0, "y": 1, "z": 2, "a": 3}
        self.rule_dict = {}
        for rule in all_rules:
            self.parse_rules(rule)
        self.space_region = {
            "x" : range(MIN_LIMITS[0], feasible_space[0]),
            "y" : range(MIN_LIMITS[1], feasible_space[1]),
            "z" : range(MIN_LIMITS[2], feasible_space[2]),
            "a" : range(MIN_LIMITS[3], feasible_space[3] -1)
        }
        self.all_coords = list(product(self.space_region['x'], self.space_region['y'], \
                                self.space_region['z'], self.space_region['a']))

    def parse_rules(self, rule):

        # Split rule into rule number and description
        rule_no_str, info = rule.split(': ', 1)
        rule_no = int(rule_no_str.strip("RULE "))

        # Regex to extract coefficients and velocity
        pattern = (
            r"(\d+)x\+(\d+)y\+(\d+)z\+(\d+)a DIVIDE (\d+) HAS REMAINDER (\d+)"
            r" \| DEBRIS VELOCITY \((-?\d+), (-?\d+), (-?\d+), (-?\d+)\)"
        )

        match = re.match(pattern, info)
        values = list(map(int, match.groups()))

        # Build parsed dictionary
        parsed_data = {
            "x": values[0], "y": values[1], "z": values[2], "a": values[3],
            "div": values[4], "rem": values[5],
            "vx": values[6], "vy": values[7], "vz": values[8], "va": values[9],
        }

        # Store in rule_dict
        self.rule_dict[rule_no] = parsed_data

    def __check_debris(self, coords, rule_no):
        rule_check = self.rule_dict[rule_no]
        debris_total = (
            (rule_check['x'] * coords[0]) + (rule_check['y'] * coords[1]) +\
            (rule_check['z'] * coords[2]) + (rule_check['a'] * coords[3])
            )
        if (debris_total % rule_check["div"]) == rule_check["rem"]:
            return True
        else:
            return False

    def count_debris(self):
        debris_map = []
        for coords in self.all_coords:
            for rule_no in self.rule_dict:
                check = self.__check_debris(coords, rule_no)
                if check:
                    debris_map.append((rule_no, coords))
        self.debris_map = debris_map
        return len(debris_map)

    def __wrapped_move(self, pos, delta, dim, wrapping):
        min_val = min(self.space_region[dim])
        max_val = max(self.space_region[dim])
        range_size = len(self.space_region[dim])
        new_pos = pos + delta

        if wrapping:
            return (new_pos - min_val) % range_size + min_val
        elif min_val <= new_pos <= max_val:
            return new_pos
        else:
            return pos  # No movement if out-of-bounds

    def __move_particle(self, rule, particle, time = 1, wrapping = True):
        new_coords = []
        for dim, idx in self.idx_map.items():
            velocity = self.rule_dict[rule]["v" + dim]
            delta = velocity * time
            moved_pos = self.__wrapped_move(particle[idx], delta, dim, wrapping)
            new_coords.append(moved_pos)
        return tuple(new_coords)

    def __move_in_dimension(self, coords, move, time = 1, wrapping = False):
        dim, velocity = move
        dim_idx = self.idx_map[dim]
        delta = velocity * time
        new_coords = list(coords).copy()
        new_coords[dim_idx] = self.__wrapped_move(coords[dim_idx], delta, dim, wrapping)
        return tuple(new_coords)

    def find_flight_path(self, target, start=(0, 0, 0, 0)):
        ALL_MOVES = list(product(("x", "y", "z"), (1, -1, 0)))
        MAX_TIME = 200  # upper limit to search; tweak as needed
        og_debris_map = self.debris_map.copy()

        # Precompute debris positions per timestep
        debris_by_time = {0: og_debris_map}
        for t in range(1, MAX_TIME + 1):
            for rule, pos in og_debris_map:
                debris_pos = self.__move_particle(rule, pos, t)
                debris_by_time.setdefault(t, set()).add(debris_pos)

        # Dijkstra/BFS with time dimension
        heap = [(0, start)]  # (time, position)
        visited = set()  # track (position, time)

        while heap:
            time, pos = heapq.heappop(heap)

            if pos == target:
                return time

            if (pos, time) in visited:
                continue
            visited.add((pos, time))

            next_time = time + 1
            if next_time in debris_by_time:
                occupied = debris_by_time[next_time]
            else:
                debris_by_time[next_time] = {
                    self.__move_particle(rule, pos, next_time)
                        for rule, pos in og_debris_map
                }

            for move in ALL_MOVES:
                next_pos = self.__move_in_dimension(pos, move, 1)
                if next_pos not in occupied or next_pos == start:
                    heapq.heappush(heap, (next_time, next_pos))

        return -1  # if unreachable

sub = Submarine(input_data, feasible)

debris = sub.count_debris()
print("Part 1:", debris)

flight_time = sub.find_flight_path(target_coords)
print("Part 2:", flight_time)

print(f"Execution Time = {time.time() - start_time:.5f}s")
