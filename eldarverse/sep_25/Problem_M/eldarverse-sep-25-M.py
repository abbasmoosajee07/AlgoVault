"""Eldarverse Puzzles - Problem M
Solution Started: September 7,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-M
Solution by: Abbas Moosajee
Brief: [Triangle Cutting]"""

#!/usr/bin/env python3
from pathlib import Path
from math import sqrt

# Load input file
input_file = "problem-sep-25-long-M-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def calculate_area(a, b):
    return 1/2 * a * b

def cut_triangles(adj, opp):
    # altitude from right angle to hypotenuse
    hyp = sqrt(adj**2 + opp**2)
    h = (adj * opp) / hyp
    d1 = (adj**2) / hyp
    d2 = (opp**2) / hyp
    return (h, d1), (h, d2)

def total_cuts(A, B, MAX_K):
    queue = [(A, B, 0)]
    max_areas = []
    while queue:
        A, B, K = queue.pop()
        if K >= MAX_K:
            area = calculate_area(A, B)
            max_areas.append(area)
            continue
        cuts = cut_triangles(A, B)
        for a, b in cuts:
            queue.append((a, b, K + 1))
            # print(f"{a=} {b=} {calculate_area(a, b)}")
    return max(max_areas)

solutions = []
for case_no, case_data in enumerate(data[1:], 1):
    A, B, K = tuple(map(int, case_data.split()))
    max_area = total_cuts(A, B, K)
    solutions.append(f"Case #{case_no}: {max_area:.6f}")
    print(solutions[-1])

output_file = "problem-sep-25-long-M-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))
