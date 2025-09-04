"""Eldarverse Puzzles - Problem C
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-C
Solution by: Abbas Moosajee
Brief: [Typehead Search]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-sep-25-long-C-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
solutions = ["Case #1:"]


def parse_data(input):
    no_keys = int(input[0])
    keywords = []
    actions = ""
    for line_no, line_data in enumerate(input[1:]):
        if line_no < no_keys:
            keywords.append(line_data)
        elif not line_data.startswith("==="):
            actions = line_data

    return keywords, list(actions)

keywords, actions = parse_data(data)

current_text = ""

while actions:
    use_action = actions.pop(0)
    if use_action == "<" and len(current_text) >= 1:
        current_text = current_text[:-1]
    else:
        current_text+= use_action
    count = 0
    for word in keywords:
        if word.startswith(current_text):
            count += 1
    if len(current_text) >= 3:
        solutions.append(str(count))

print(solutions)

output_file = "problem-sep-25-long-C-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("\n".join(solutions))