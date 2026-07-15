"""FlipFlop Codes Puzzles - Puzzle 04
Solution Started: July 15, 2026
Puzzle Link: https://flipflop.slome.org/2025/4
Solution by: Abbas Moosajee
Brief: [Beach Cleanup]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque

# Load input file
input_file = "puzzle_04_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def calc_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def calc_shortest_distance(p1, p2):
    steps = 0
    valid_moves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    queue = deque([(p1, 0)])
    visited = set(p1)
    while queue:
        point, steps = queue.popleft()
        if point == p2:
            return steps
        for dx, dy in valid_moves:
            nx, ny = point[0] + dx, point[1] + dy
            npoint = (nx, ny)
            if 0 <= nx < 101 and 0 <= ny < 101 and npoint not in visited:
                queue.append((npoint, steps + 1))
                visited.add(npoint)
    return -1

def sort_trash(trash_list):
    points = [tuple(map(int, p.split(","))) for p in trash_list]
    return sorted(points, key=lambda p: calc_distance((0, 0), p))

steps_p1 = 0
steps_p2 = 0
last_point = (0, 0)

for point_str in data[:]:
    next_point = tuple(map(int, point_str.split(",")))
    steps_p1 += calc_distance(last_point, next_point)
    steps_p2 += calc_shortest_distance(last_point, next_point)
    last_point = next_point

steps_p3 = 0
last_point = (0, 0)
for next_point in sort_trash(data):
    steps_p3 += calc_shortest_distance(last_point, next_point)
    last_point = next_point

print("FlpFlops 25, Puzzle 04")
print("Part 1:", steps_p1)
print("Part 2:", steps_p2)
print("Part 3:", steps_p3)

