"""AquaQ Puzzles - Puzzle 1
Solution Started: September 62025,
Puzzle Link: https://challenges.aquaq.co.uk/challenge/1
Solution by: Abbas Moosajee
Brief: [Rose by any other name]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Challenge_01_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

HEXADECIMAL_CHARS = "0123456789abcdef"

def to_hex_string(s: str) -> str:
    """Replace non-hex chars with '0'."""
    return "".join(c if c in HEXADECIMAL_CHARS else "0" for c in s)

def pad_to_next_multiple_of_3(s: str, pad_char="X") -> str:
    """Pad string length up to nearest multiple of 3."""
    pad_len = (3 - len(s) % 3) % 3
    return s + pad_char * pad_len

def process_string(data: str) -> str:
    hex_chars = to_hex_string(data)
    padded = pad_to_next_multiple_of_3(hex_chars)
    split_size = len(padded) // 3

    # take first 2 chars of each section
    sections = [padded[i:i+split_size] for i in range(0, len(padded), split_size)]
    return "".join(sec[:2] for sec in sections)

# Example
final_string = process_string(data[0])
print("Challenge 01:", final_string)
