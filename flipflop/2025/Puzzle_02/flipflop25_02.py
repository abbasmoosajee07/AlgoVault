"""FlipFlop Codes Puzzles - Puzzle 02
Solution Started: July 13, 2026
Puzzle Link: https://flipflop.slome.org/2025/2
Solution by: Abbas Moosajee
Brief: [Rollercoaster Heights]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_02_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read()

move_dict = {"^": +1, "v": -1}

height_p1 = 0
max_height_p1 = 0

height_p2 = 0
max_height_p2 = 0

height_p3 = 0
max_height_p3 = 0

height_jump = 0
last_move = data[0]

def nth_fibonacci(n):
    # base case
    if n <= 1:
        return n
    # sum of the two preceding 
    # Fibonacci numbers
    return nth_fibonacci(n - 1) + nth_fibonacci(n - 2)

for idx, move in enumerate(data, start=1):
    height_p1 += move_dict[move]
    max_height_p1 = max(height_p1, max_height_p1)

    if last_move == move:
        height_jump += 1
    elif last_move != move:
        height_p3 +=  nth_fibonacci(height_jump) * move_dict[last_move]
        max_height_p3 = max(height_p3, max_height_p3)
        height_jump = 1

    height_p2 += height_jump * move_dict[move]
    max_height_p2 = max(height_p2, max_height_p2)

    last_move = move

print("FlipFlop 25, Puzzle 02")
print("Part 1:", max_height_p1)
print("Part 2:", max_height_p2)
print("Part 3:", max_height_p3)

