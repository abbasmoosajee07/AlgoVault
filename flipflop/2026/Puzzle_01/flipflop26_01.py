"""FlipFlop 2026: BitFlop Internship - Puzzle 1
Solution Started: July 17, 2026
Puzzle Link: https://flipflop.slome.org/2026/1
Solution by: Abbas Moosajee
Brief: [Coffee Brewing]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_01_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

time_p1, time_p2, time_p3 = (0, 0, 0)

def perfect_coffee(current, target = 60):
    heat_time, cool_time = (0, 0)
    if current <= target:
        heat_time = target - current
    else:
        cool_time = (current - target) * 5
    return heat_time, cool_time

for temp_str in data:
    heat, cool = perfect_coffee(int(temp_str))
    time_p1 += heat
    time_p2 += heat + cool

split_data = int(len(data) / 2)
for (coffee, target) in zip(data[:split_data], data[split_data:]):
    heat, cool = perfect_coffee(int(coffee), int(target))
    time_p3 += (heat + cool)

print("FlipFlop 2026, Puzzle 01")
print("Part 1:", time_p1)
print("Part 2:", time_p2)
print("Part 3:", time_p3)

