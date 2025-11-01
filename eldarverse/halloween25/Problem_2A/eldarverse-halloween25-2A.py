"""Eldarverse Puzzles - Problem 2A
Solution Started: October 28,
Puzzle Link: https://www.eldarverse.com/problem/halloween25-2A
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-halloween25-2A-input1.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def parse_raw_data(raw_data):
    parsed_data = []
    for test_no in range(1, len(raw_data), 2):
        NM_ints = tuple(map(int, raw_data[test_no].split()))
        movements = raw_data[test_no + 1].split()
        parsed_data.append((NM_ints, movements))
    return parsed_data

def run_ghost_sim(N, M, ghosts):
    total_cells = list(range(0, N))
    all_states = set()
    ans = "NO"
    ghost_data = [(int(ghost_n[0]), ghost_n[1]) for ghost_n in ghosts]
    while True:
        for ghost_no in enumerate(M):
            pos, dir = ghost_data[ghost_no]
            
    print(N, total_cells)
    return ans
test_cases = parse_raw_data(data)
solutions = []

for case_no, ((N, M), ghosts) in enumerate(test_cases[:], start=1):
    case_result = run_ghost_sim(N, M, ghosts)
    solutions.append(f"Case #{case_no}: {case_result}")
    print(solutions[-1])

# output_file = "problem-halloween25-2A-output.txt"
# output_path = Path(__file__).parent / output_file
# with output_path.open("w", encoding="utf-8") as f:
#     f.write("\n".join(solutions) + "\n")