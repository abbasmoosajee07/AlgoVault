"""AquaQ Puzzles - Puzzle 0
Solution Started: September 62025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/0
Solution by: Abbas Moosajee
Brief: [What's a Numpad]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Challenge_00_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

T9_DICT = {
    2: "abc", 3: "def",
    4: "ghi", 5: "jkl",
    6: "mno", 7: "pqrs",
    8: "tuv", 9:  "wxyz",
    1: " ", 0: " ",
}

message = ""
for entry in data:
    key, press = tuple(map(int, entry.split()))
    all_letters = T9_DICT[key]
    char = all_letters[press - 1]
    message += char

print("Challenge 0:", message)
