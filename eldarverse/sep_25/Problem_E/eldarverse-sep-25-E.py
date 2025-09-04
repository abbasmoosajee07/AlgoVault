"""Eldarverse Puzzles - Problem E
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-E
Solution by: Abbas Moosajee
Brief: [Manao and the Magical Stones]"""

#!/usr/bin/env python3
from pathlib import Path
from math import floor, pow, isqrt
# Load input file
input_file = "problem-sep-25-long-E-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
    n_stones = list(map(int, data[1:]))
n_stones2 = [1, 12]

def calculate_energy(N):
    total = 0
    for i in range(N+1):
        i_energy = pow(i, 1/2)
        total += floor(i_energy)
    return total

def calculate_energy_fast(N):
    total = 0
    max_k = isqrt(N)   # floor(sqrt(N))
    for k in range(max_k + 1):
        # number of i's with floor(sqrt(i)) = k
        start = k * k
        end = min((k+1)**2 - 1, N)
        count = end - start + 1
        total += k * count
    return total

solutions = []

for case_no, N in enumerate(n_stones, start=1):
    energy = calculate_energy_fast(N)
    solutions.append(f"Case #{case_no}: {energy}")
    print(solutions[-1])

output_file = "problem-sep-25-long-E-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")
