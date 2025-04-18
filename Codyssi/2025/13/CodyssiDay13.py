"""Codyssi Puzzles - Problem 13
Solution Started: Apr 15, 2025
Puzzle Link: https://www.codyssi.com/view_problem_17?
Solution by: Abbas Moosajee
Brief: [Laestrygonian Guards]
"""

#!/usr/bin/env python3

import os, re, copy, heapq
import numpy as np
from collections import defaultdict, deque

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n')
    ship_paths = {(arr, des) :int(dist) for line in input_data
                    for (arr,_,des,_,dist) in [line.split(' ')]}

def build_graph(path_lines):
    graph = defaultdict(list)
    for (src, dest), weight in path_lines.items():
        graph[src].append((dest, weight))
    return graph

def find_basic_paths(loc_dict, start):
    queue = deque([[start]])
    visited = set([start])
    total_paths = {start: [start]}
    while queue:
        path = queue.popleft()
        for neighbor, _ in loc_dict.get(path[-1], []):
            if neighbor not in visited:
                new_path = path + [neighbor]
                total_paths[neighbor] = new_path
                visited.add(neighbor)
                queue.append(new_path)
    return total_paths

loc_graph = build_graph(ship_paths)

possible_paths = find_basic_paths(loc_graph, "STT")
longest_paths = [len(path) - 1 for path in possible_paths.values()]
print("Part 1:", np.prod(sorted(longest_paths)[-3:]))

def find_weighted_paths(graph, start):
    queue = deque([(0, start)])
    all_paths = {start: 0}
    while queue:
        curr_dist, curr_node = queue.popleft()
        for neighbor, weight in graph.get(curr_node, []):
            dist = curr_dist + weight
            if neighbor not in all_paths or dist < all_paths[neighbor]:
                all_paths[neighbor] = dist
                queue.append((dist, neighbor))
    return all_paths

shortest_paths = find_weighted_paths(loc_graph, 'STT')
print("Part 2:", np.prod(sorted(shortest_paths.values())[-3:]))

def identify_cycles(graph):
    def dfs(node, start, path, total):
        for dest, dist in graph.get(node, []):
            if dest == start:
                # Found a cycle
                cycle_lens.append(total + dist)
            elif dest not in path:
                dfs(dest, start, path + [dest], total + dist)

    cycle_lens = []
    for start in graph:
        dfs(start, start, [start], 0)
    return cycle_lens

cycle_lens = identify_cycles(loc_graph)
print("Part 3:", max(cycle_lens))