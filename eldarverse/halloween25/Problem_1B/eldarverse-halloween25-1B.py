"""Eldarverse Puzzles - Problem 1B
Solution Started: October 27,
Puzzle Link: https://www.eldarverse.com/problem/halloween25-1B
Solution by: Abbas Moosajee
Brief: [Werewolf Scribes (part 1)]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
from itertools import chain

# Load input file
input_file = "problem-halloween25-1B-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def calculate_strength(total_nights, pattern, A, B, M):
    def strength_eq(xi_1 = 0):
        return ((xi_1 * A) + B) % (2 ** 20)

    median_history = []
    clan_dict = defaultdict(list)
    prev_strength = 0
    for night_i in range(1,  total_nights + 1):
        wolf_i = (night_i - 1) % len(pattern)
        wolf = int(pattern[wolf_i])
        wolf_strength = strength_eq(prev_strength)
        clan_dict[wolf].append(wolf_strength)
        prev_strength = wolf_strength
        # print(f"{night_i=}, {wolf=}, {wolf_strength=}")
        if night_i % M == 0:
            clan_members = clan_dict[wolf]
            new_list = []
            for mem_inc in clan_members:
                new_list.append(mem_inc + 1)
            clan_dict[wolf] = new_list
        median_strength = median(list(chain.from_iterable(clan_dict.values())))
        median_history.append(median_strength)
    return median_history

def median(data):
    sorted_data = sorted(data)
    n = len(data)
    if n % 2 == 1:  # Odd length
        median_value = sorted_data[n // 2]
    else:  # Even length
        median_value = sorted_data[n // 2 - 1]
    return median_value

solutions = []

for case_no, case_data in enumerate(data[1:], start=1):
    N, A, B, M, S = case_data.split(" ")
    case_strength = calculate_strength(int(N), list(S), int(A), int(B), int(M))
    solutions.append(f"Case #{case_no}: {sum(case_strength)}")

output_file = "problem-halloween25-1B-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")

