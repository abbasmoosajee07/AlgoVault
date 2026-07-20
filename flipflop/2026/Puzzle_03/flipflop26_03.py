"""FlipFlop 2026: BitFlop Internship - Puzzle 3
Solution Started: July 18, 2026
Puzzle Link: https://flipflop.slome.org/2026/3
Solution by: Abbas Moosajee
Brief: [Password Competition]"""

#!/usr/bin/env python3
from pathlib import Path
from itertools import groupby

# Load input file
input_file = "puzzle_03_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def filter_password(input, func):
    best_password = ["", 0]
    for password in input:
        strength = func(password)
        if strength > best_password[1]:
            best_password = (password, strength)
    return best_password

def calc_score_p1(pass_str):
    pass_len = len(pass_str)
    checks = {"upper": 0, "lower": 0, "digit": 0}
    for char in pass_str:
        if checks['upper'] == 0 and char.isupper():
            checks['upper'] = 1
        elif checks['lower'] == 0 and char.islower():
            checks['lower'] = 1
        elif checks['digit'] == 0 and char.isdigit():
            checks['digit'] = 1
    return pass_len * sum(checks.values())

def calc_score_p2(pass_str):
    def consecutive_repeat_score(pass_str):
        max_run = max((len(list(g)) for _, g in groupby(pass_str)), default=0)
        return max_run ** 2 if max_run >= 3 else 0
    pass_len = len(pass_str)
    color_mult = 1
    checks = {"upper": 0, "lower": 0, "digit": 0, "7": 0, "seqn": 0}
    for char in pass_str:
        if checks['upper'] == 0 and char.isupper():
            checks['upper'] = 1
        elif checks['lower'] == 0 and char.islower():
            checks['lower'] = 1
        elif checks['digit'] == 0 and char.isdigit():
            checks['digit'] = 1
    if "7" in pass_str and not any(c.isdigit() and c != "7" for c in pass_str):
        checks['7'] = 7
    checks['seqn'] += consecutive_repeat_score(pass_str)
    color_mult = 3 if any(word in pass_str for word in ("red", "blue", "green")) else 1
    return pass_len * sum(checks.values()) * color_mult

def maximise_strength(pass_inp, func):
    change = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    max_strength = 0
    for nchar in change:
        strength = 0
        for pass_str in pass_inp:
            new_pass = pass_str + nchar
            strength += func(new_pass)
        max_strength = max(max_strength, strength)
        # print(nchar, strength, max_strength)
    return max_strength

print("FlipFlops 26, Puzzle 03")
print("Part 1:", filter_password(data, calc_score_p1)[0])
print("Part 2:", filter_password(data, calc_score_p2)[0])
print("Part 3:", maximise_strength(data, calc_score_p2))

