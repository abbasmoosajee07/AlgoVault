"""FlipFlop 2026: BitFlop Internship - Puzzle 5
Solution Started: July 21, 2026
Puzzle Link: https://flipflop.slome.org/2026/5
Solution by: Abbas Moosajee
Brief: [One Way City]"""

#!/usr/bin/env python3
from pathlib import Path
from queue import Queue

# Load input file
input_file = "puzzle_05_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class StreetNavigator:
    MOVES = {">": (0, 1), "<":(0,-1), "v":(1,0), "^": (-1,0)}
    ILLEGAL_TURNS = {"^":">", ">":"v", "v":"<", "<":"^"}

    def __init__(self, data_inp):
        self.grid_dict = self.build_grid(data_inp)

    @staticmethod
    def build_grid(grid_data):
        grid_dict = {}
        for row_no, row in enumerate(grid_data):
            for col_no, char in enumerate(row):
                grid_dict[(row_no, col_no)] = char
        return grid_dict

    def print_grid(self, visited = {}, baseGrid = False):
        grid_dict = self.grid_dict
        max_row = max(r for r, c in grid_dict)
        max_col = max(c for r, c in grid_dict)
        print_data = []
        for row_no in range(max_row + 1):
            row_data = ""
            for col_no in range(max_col + 1):
                coord = (row_no, col_no)
                if baseGrid:
                    row_data += grid_dict[coord]
                else:
                    row_data += grid_dict[coord] if coord in visited else "."
            print_data.append(row_data)
        print("Visited No:", len(visited))
        print("\n".join(print_data))

    def traverse_grid(self, start_pos=(0, 0), direction_change=False, no_illegal=False):
        max_row = max(r for r, c in self.grid_dict)
        max_col = max(c for r, c in self.grid_dict)

        def is_edge(pos):
            return pos[0] in (0, max_row) or pos[1] in (0, max_col)

        max_score = 0
        # queue entries: (pos, score, has_made_change, right_turns_made, seen frozenset)
        queue = Queue()
        queue.put((start_pos, 0, False, 0, frozenset()))

        while not queue.empty():
            pos, score, has_made_change, illegal_turns, seen = queue.get()
            symbol = self.grid_dict[pos]

            if pos in seen:
                max_score = max(max_score, score)
                if no_illegal and not is_edge(pos) and illegal_turns < 3:
                    turned = self.ILLEGAL_TURNS[symbol]
                    dr, dc = self.MOVES[turned]
                    npos = (pos[0] + dr, pos[1] + dc)
                    queue.put((npos, score, has_made_change, illegal_turns + 1, seen))
                continue

            new_seen = seen | {pos}
            score += 1

            if direction_change:
                if is_edge(pos):
                    dr, dc = self.MOVES[symbol]
                    npos = (pos[0] + dr, pos[1] + dc)
                    queue.put((npos, score, has_made_change, illegal_turns, new_seen))
                    continue
                if not has_made_change:
                    for dirr in self.MOVES:
                        dr, dc = self.MOVES[dirr]
                        npos = (pos[0] + dr, pos[1] + dc)
                        queue.put((npos, score, dirr != symbol, illegal_turns, new_seen))
                    continue
                dr, dc = self.MOVES[symbol]
                npos = (pos[0] + dr, pos[1] + dc)
                queue.put((npos, score, has_made_change, illegal_turns, new_seen))
            else:
                dr, dc = self.MOVES[symbol]
                npos = (pos[0] + dr, pos[1] + dc)
                queue.put((npos, score, True, illegal_turns, new_seen))

        return max_score

streets = StreetNavigator(data)

print("FlipFlops 2026, Puzzle 05")
print("Part 1:", streets.traverse_grid())
print("Part 2:", streets.traverse_grid(direction_change=True))
print("Part 3:", streets.traverse_grid(direction_change=True, no_illegal=True))
