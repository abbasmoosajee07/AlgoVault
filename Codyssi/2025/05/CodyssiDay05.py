"""Codyssi Puzzles - Problem 5
Solution Started: Apr 8, 2025
Puzzle Link: https://www.codyssi.com/view_problem_9?
Solution by: Abbas Moosajee
Brief: [Patron Islands]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split('\n')
    island_coords = [tuple(map(int, coords.strip("()").split(","))) for coords in input_data]

min_dist = float('inf')
max_dist = float('-inf')

for x, y in island_coords:
    dist = abs(x) + abs(y)
    max_dist = max(max_dist, dist)
    if dist <= min_dist:
        min_dist = min(min_dist, dist)
        closest = (x, y)

print("Part 1:", max_dist - min_dist)

min_dist = [abs(x - closest[0]) + abs(y - closest[1]) for x, y in island_coords if (x, y) != closest]
print("Part 2:", min(min_dist))

prev_island = (0, 0)
travel_distance = []
visited_islands = set(island_coords)

while visited_islands:
    # Initialize the closest island info
    min_dist = float('inf')

    # Iterate over the remaining unvisited islands
    for x, y in visited_islands:
        distance = abs(x - prev_island[0]) + abs(y - prev_island[1])

        # Update the closest island, considering ties by x and y coordinates
        if distance < min_dist or \
            (distance == min_dist and (x < next_island[0] or \
                (x == next_island[0] and y < next_island[1]))):
            min_dist = distance
            next_island = (x, y)

    # Output the closest island and distance to it
    # print(f"Traveling to island {next_island} with distance {min_dist}")

    # Remove the selected island from visited islands and update the travel distance
    visited_islands.remove(next_island)
    travel_distance.append(min_dist)

    # Update the current position
    prev_island = next_island

print("Part 3:", sum(travel_distance))