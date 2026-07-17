"""FlipFlop Codes Puzzles - Puzzle 06
Solution Started: July 16, 2026
Puzzle Link: https://flipflop.slome.org/2025/6
Solution by: Abbas Moosajee
Brief: [Bird Spotters]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_06_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class BirdMap:
    sky = (1000, 1000)
    frame = {"start" :(250, 250), "size": (500, 500)}
    def __init__(self, bird_str):
        self.all_birds = [tuple(map(int, p.split(","))) for p in bird_str]

    def calc_pos(self, bird, t):
        # assume start = (0,0)
        xv, yv = bird
        ex, ey = self.sky
        return (xv * t) % ex, (yv * t) % ey

    def within_frame(self, x, y):
        xi, yi = self.frame["start"]
        xs, ys = self.frame["size"]
        if xi <= x < xi + xs and yi <= y < yi + ys:
            return True
        else:
            return False

    def photograph(self, t=100):
        count = 0
        for bird_speed in self.all_birds:
            nx,  ny = self.calc_pos(bird_speed, t)
            if self.within_frame(nx, ny):
                count += 1
        return count

    def multiple_pics(self, total, time_gap):
        birds_seen = 0
        for pic_no in range(1, total + 1):
            birds_seen += self.photograph(time_gap * pic_no)
            # print(pic_no, birds_seen)
        return birds_seen

birds = BirdMap(data)

print("FlipFlops 25, Puzzle 06")
print("Part 1:", birds.photograph(100))
print("Part 2:", birds.multiple_pics(1000, 3600))
print("Part 3:", birds.multiple_pics(1000, 31556926))
