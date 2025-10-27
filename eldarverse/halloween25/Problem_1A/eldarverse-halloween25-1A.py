"""Eldarverse Puzzles - Problem 1A
Solution Started: October 27,
Puzzle Link: https://www.eldarverse.com/problem/halloween25-1A
Solution by: Abbas Moosajee
Brief: [Werewolf Clans]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-halloween25-1A-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def build_clans(total_nights, pattern):
    clan_dict = {int(clan_no): 0 for  clan_no in pattern}
    for night_i in range(total_nights):
        wolf_i = (night_i + 0) % len(pattern)
        wolf = int(pattern[wolf_i])
        clan_dict[wolf] += 1
    return set(clan_dict.values())

solutions = []

for case_no, case_data in enumerate(data[1:], start=1):
    N, S = case_data.split(" ")
    case_clan = build_clans(int(N), list(S))
    solutions.append(f"Case #{case_no}: {max(case_clan)} {min(case_clan)}")

output_file = "problem-halloween25-1A-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions) + "\n")