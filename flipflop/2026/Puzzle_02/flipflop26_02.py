"""FlipFlop 2026: BitFlop Internship - Puzzle 2
Solution Started: July 17, 2026
Puzzle Link: https://flipflop.slome.org/2026/2
Solution by: Abbas Moosajee
Brief: [Lasering Walls]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_02_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read()

MOVE_DICT  = {"<":-1, ">":+1}

def laser_wall(instructions, wall_size = 100):
    wall_segs = [0] * wall_size
    next_idx = 0
    for move in instructions:
        next_idx = (next_idx + MOVE_DICT[move]) % wall_size
        wall_segs[next_idx] += 1
    idx, mx = max(enumerate(wall_segs), key=lambda x: x[1])
    return  mx * (idx + 1)

def laser_robot_wall(instructions, wall_size = 100):
    laser_idx, robot_idx, wall_temp= (0, 0, 0)
    for (laser, robot) in zip(instructions, instructions[::-1]):
        laser_idx = (laser_idx + MOVE_DICT[laser]) % wall_size
        robot_idx = (robot_idx + MOVE_DICT[robot]) % wall_size
        wall_temp += 1 if laser_idx == robot_idx else 0
    return  wall_temp

def laser_moving_wall(instructions, wall_size = 100):
    wall_dict = {no: (no, 0) for no in range(1, wall_size + 1)}
    laser_idx  = 1
    for (laser, robot) in zip(instructions, instructions[::-1]):
        laser_idx = (laser_idx + MOVE_DICT[laser]) % wall_size
        for wall_id, (pos, temp) in wall_dict.items():
            npos = (pos + MOVE_DICT[robot]) % wall_size
            temp += 1 if laser_idx == npos else 0
            wall_dict[wall_id] = (npos, temp)
    seg_id, (_, temp) = max(wall_dict.items(), key=lambda item: item[1][1])
    return  seg_id * temp

print("FlipFlops 2026, Puzzle 02")
print("Part 1:", laser_wall(data))
print("Part 2:", laser_robot_wall(data))
print("Part 3:", laser_moving_wall(data))