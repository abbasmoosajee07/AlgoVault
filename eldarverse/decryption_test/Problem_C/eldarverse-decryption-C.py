"""Eldarverse Puzzles - Problem C
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-C
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import Counter

# Load input file
input_file = "problem-decryption-contest-1-C-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def english_frequencies():
    return {
        'a': 0.07743208627550165, 'b': 0.01402241586697527,
        'c': 0.02665670667329359, 'd': 0.04920785702311875,
        'e': 0.13464518994079883, 'f': 0.025036247121552113,
        'g': 0.017007472935972733,'h': 0.05719839895067157,
        'i': 0.06294794236928244, 'j': 0.001267546400727001,
        'k': 0.005084890317533608,'l': 0.03706176274237046,
        'm': 0.030277007414117114,'n': 0.07125316518982316,
        'o': 0.07380002176297765, 'p': 0.017513315119093483,
        'q': 0.0009499245648139707,'r': 0.06107162078305546,
        's': 0.061262782073188304,'t': 0.08760480785349399,
        'u': 0.030426995503298266,'v': 0.01113735085743191,
        'w': 0.02168063124398945, 'x': 0.0019880774173815607,
        'y': 0.022836421813561863,'z': 0.0006293617859758195,
    }

def chi_square(text: str) -> float:
    freqs = english_frequencies()
    length = len(text)
    if length == 0:
        return float("inf")  # avoid division by zero

    counts = Counter(text.lower())
    score = 0.0

    for letter, expected in freqs.items():
        actual = counts.get(letter, 0) / length
        err = abs(expected - actual)
        score += err
    return score

T = int(data[0])
texts = []
current = []
for line in data[1:]:
    if line.startswith("="):
        texts.append("\n".join(current[:]))
        current = []
    else:
        current.append(line)
texts.append("\n".join(current))

print(texts[3])
solutions = []
output_file = "problem-decryption-contest-1-C-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("".join(solutions))