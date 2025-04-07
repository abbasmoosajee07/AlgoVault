"""Codyssi Puzzles - Problem 4
Solution Started: Apr 6, 2025
Puzzle Link: https://www.codyssi.com/view_problem_4?
Solution by: Abbas Moosajee
Brief: [CTraversing the Country]
"""

#!/usr/bin/env python3

import os, re, copy
from collections import deque, defaultdict

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n')
    area_map = [(loc_1, loc_2) for line in input_data for loc_1, loc_2 in [line.split(" <-> ")]]

loc_dict = defaultdict(list)
for loc_1, loc_2 in area_map:
    loc_dict[loc_1].append(loc_2)
    loc_dict[loc_2].append(loc_1)

def find_shortest_paths(loc_dict, start):
    queue = deque([[start]])
    visited = set([start])
    shortest_paths = {start: [start]}

    while queue:
        path = queue.popleft()
        current = path[-1]
        for neighbor in loc_dict.get(current, []):
            if neighbor not in visited:
                new_path = path + [neighbor]
                shortest_paths[neighbor] = new_path
                visited.add(neighbor)
                queue.append(new_path)

    return shortest_paths

possible_paths = find_shortest_paths(loc_dict, "STT")

loc_set = {loc for loc_pair in area_map for loc in loc_pair}
print("Part 1:", len(loc_set))

short_paths = [path for path in possible_paths.values() if len(path) <= 4]
print("Part 2:", len(short_paths))

travel_time = [len(path) for path in possible_paths.values()]
print("Part 3:", sum(travel_time) - len(travel_time))