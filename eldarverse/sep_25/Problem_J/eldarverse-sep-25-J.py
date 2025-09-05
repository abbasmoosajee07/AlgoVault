"""Eldarverse Puzzles - Problem J
Solution Started: September 5,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-J
Solution by: Abbas Moosajee
Brief: [Polyline]"""

#!/usr/bin/env python3
from pathlib import Path
from math import hypot, cos, sin, pi

# Load input file
input_file = "problem-sep-25-long-J-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def parse_raw_data(raw_data):
    parsed_data = []
    new_test = True
    for line_no, line_data in enumerate(raw_data[1:], 1):
        if new_test:
            segments = []
            new_test = False
            segment_mark = int(line_data) + line_no
        elif line_no <= segment_mark:
            segments.append(tuple(map(int, line_data.split())))
            if line_no == segment_mark:
                parsed_data.append(segments)
                new_test = True
    return parsed_data



    def maximise_distance(self, vectors):
        import math
        best = 0.0
        # sample 720 directions (every 0.5 degrees)
        for k in range(720):
            theta = 2 * math.pi * k / 720
            dx = math.cos(theta)
            dy = math.sin(theta)

            sx, sy = 0.0, 0.0
            for x, y in vectors:
                # choose sign that aligns with (dx,dy)
                if x*dx + y*dy >= 0:
                    sx += x
                    sy += y
                else:
                    sx -= x
                    sy -= y

            best = max(best, math.hypot(sx, sy))
        return best

def maximise_distance(vectors):
    best = 0.0
    # sample 720 directions (every 0.5 degrees)
    for k in range(720):
        theta = 2 * pi * k / 720
        dx = cos(theta)
        dy = sin(theta)

        sx, sy = 0.0, 0.0
        for x, y in vectors:
            # choose sign that aligns with (dx,dy)
            if x*dx + y*dy >= 0:
                sx += x
                sy += y
            else:
                sx -= x
                sy -= y

        best = max(best, hypot(sx, sy))
    return best

test_cases = parse_raw_data(data)
solutions = []
for case_no, segments in enumerate(test_cases, start = 1):
    max_dist = maximise_distance(segments)
    solutions.append(f"Case #{case_no}: {max_dist:.10f}")
    print(solutions[-1])

output_file = "problem-sep-25-long-J-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))