"""FlipFlop 2026: BitFlop Internship - Puzzle 7
Solution Started: July 24, 2026
Puzzle Link: https://flipflop.slome.org/2026/7
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "puzzle_07_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().split("\n\n")

class Snake:
    DIRS = {"^": (0, 1), "v":(0,-1), "<":(-1,0), ">": (1,0)}

    def __init__(self, moves, coords, grid_size):
        self.moves = moves
        self.grid = grid_size
        self.coords = [tuple(map(int, pair.split(","))) for pair in coords.split("\n")]

    def calc_next_pos(self, pos, turn):
        dc, dr = self.DIRS[turn]
        npos = (pos[0] + dc) % self.grid[0], (pos[1] + dr) % self.grid[1]
        return npos

    def eat_sushi(self, move_limit = 250):
        sushi_eaten = 0
        pos = (0, 0)
        avail_sushi = self.coords.copy()
        next_sushi = avail_sushi.pop(0)
        for nturn in self.moves[:move_limit]:
            npos = self.calc_next_pos(pos, nturn)
            if npos == next_sushi:
                sushi_eaten += 1
                next_sushi = avail_sushi.pop(0)
            # print(pos, nturn, npos)
            pos = npos
            if len(avail_sushi) <= 0:
                break
        return sushi_eaten

    def till_death(self, break_snake = True):
        pos = (0, 0)
        snake_body = [pos]
        avail_sushi = self.coords.copy()
        next_sushi = avail_sushi.pop(0)
        self_eaten = 0
        for nidx, nturn in enumerate(self.moves):
            npos = self.calc_next_pos(pos, nturn)
            grew = npos == next_sushi
            check_body = snake_body if grew else snake_body[:-1]
            new_body = [npos] + check_body
            if npos in check_body:
                if break_snake:
                    return len(snake_body)
                else:
                    self_eaten += 1
                    cut_point = check_body.index(npos)
                    new_body = new_body[:cut_point]
            if grew:
                next_sushi = avail_sushi.pop(0) if avail_sushi else None
            snake_body = new_body
            pos = npos
        return( len(snake_body)) * self_eaten

ross_snake  = Snake(data[0], data[1], (30, 30))
print("FlipFlop 2026, Puzzle 07")
print("Part 1:", ross_snake.eat_sushi(2500))
print("Part 2:", ross_snake.till_death())
print("Part 3:", ross_snake.till_death(False))
