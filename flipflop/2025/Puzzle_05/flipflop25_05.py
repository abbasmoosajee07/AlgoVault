"""FlipFlop Codes Puzzles - Puzzle 05
Solution Started: July 15, 2026
Puzzle Link: https://flipflop.slome.org/2025/5
Solution by: Abbas Moosajee
Brief: [Strange Tunnels]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque, defaultdict

# Load input file
input_file = "puzzle_05_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read()
    data1 = "ABccksiPiBAksP"
trainline = data

def identify_stations(trainline):
    stations = defaultdict(list)
    for idx, char in enumerate(trainline):
        stations[char].append(idx)
    return stations

def traverse_line(trainline, with_power = False):
    stations = identify_stations(trainline)
    n = len(trainline)

    pointer = 0
    total_steps = 0
    visited = set()
    while True:
        char = trainline[pointer]
        positions = stations[char]
        visited.add(char)
        a, b = positions
        destination = b if pointer == a else a
        power_mult = 1
        if char.isupper() and with_power:
            power_mult = -1
        total_steps += abs(destination - pointer) * power_mult
        pointer = destination + 1

        if pointer >= n:
            break

    return total_steps, visited

steps, visited = traverse_line(trainline)
unvisited = ""
for stop in trainline:
    if stop not in visited and stop not in unvisited:
        unvisited += stop
steps_p3, _ = traverse_line(trainline, True)
print("FlpFlops 25, Puzzle 05")
print("Part 1:", steps)
print("Part 2:", unvisited)
print("Part 3:", steps_p3)


