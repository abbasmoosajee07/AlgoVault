"""Eldarverse Puzzles - Problem G
Solution Started: September 4, 2025
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-G
Solution by: Abbas Moosajee
Brief: [Permutation Lock]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-sep-25-long-G-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
    all_locks = list(map(int, data[1:]))

def construct_maxD_permutation(N: int):
    """Return a permutation of 1..N whose min adjacent diff = floor(N/2)."""
    m = N // 2
    left_start = m + (N % 2)
    left = list(range(left_start, 0, -1))
    right = list(range(N, left_start, -1))

    perm = []
    # interleave left and right: left[i], right[i], ...
    for i in range(max(len(left), len(right))):
        if i < len(left):
            perm.append(str(left[i]))
        if i < len(right):
            perm.append(str(right[i]))
    return m, ' '.join(perm)

solutions = []
for lock_no, lock_size in enumerate(all_locks, start=1):
    min_diff, lock_combo = construct_maxD_permutation(lock_size)
    solutions.append(f"Case #{lock_no}: {min_diff}\n{lock_combo}")
    print(solutions[-1])

output_file = "problem-sep-25-long-G-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))
