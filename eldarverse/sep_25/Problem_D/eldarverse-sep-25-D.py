"""Eldarverse Puzzles - Problem D
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-D
Solution by: Abbas Moosajee
Brief: [Lots of Rectangles]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-sep-25-long-D-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
    rectangle_divs = list(map(int, data[1:]))

solutions = []

def rectangle_count(n: int, mod: int) -> int:
    pow2_n   = pow(2, n, mod)       # 2^n mod mod
    pow2_nm1 = pow(2, n-1, mod)     # 2^(n-1) mod mod
    val = (pow2_nm1 * (pow2_n + 1)) % mod
    return (val * val) % mod

for case_no, divs in enumerate(rectangle_divs, start=1):
    total = rectangle_count(divs, 1_000_000_009)# % 1_000_000_009
    solutions.append(f"Case #{case_no}: {total}")
    print(solutions[-1])

output_file = "problem-sep-25-long-D-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")
