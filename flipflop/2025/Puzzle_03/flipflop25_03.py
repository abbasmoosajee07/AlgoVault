"""FlipFlop Codes Puzzles - Puzzle 03
Solution Started: July 14, 2026
Puzzle Link: https://flipflop.slome.org/2025/3
Solution by: Abbas Moosajee
Brief: [Bush Salesman]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict

# Load input file
input_file = "puzzle_03_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def pick_color(bush):
    r, g, b = tuple(map(int, bush.split(",")))
    color = "Special"
    if r == g or r == b or b == g:
        return color
    if r > g and r > b:
        color = "Red"
    elif g > r and g > b:
        color = "Green"
    elif b > g and b > r:
        color = "Blue"
    return color

def calc_price(color_dict):
    return (color_dict["Red"] * 5) + (color_dict["Green"] * 2) + \
            (color_dict["Blue"] * 4) + (color_dict["Special"] * 10)

color_dict = defaultdict(int)
for bush_str in data[:]:
    bush_color = pick_color(bush_str)
    color_dict[bush_color] += 1
    # print(bush_str, bush_color)

print("FlpFlops 25, Puzzle 03")
print("Part 1:", Counter(data).most_common()[0][0])
print("Part 2:", color_dict["Green"])
print("Part 3:", calc_price(color_dict))
