"""FlipFlop 2026: BitFlop Internship - Puzzle 9
Solution Started: July 26, 2026
Puzzle Link: https://flipflop.slome.org/2026/9
Solution by: Abbas Moosajee
Brief: [Thinking With Mazes]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
# Load input file
input_file = "puzzle_09_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

data1 = ['###########', '#S#.#...#.#', '#.#.#.###.#', '#.#.......#', '#.#.#.#####', '#...#.#..E#', '###.#.#.###', '#...#.#...#', '#.###.#.#.#', '#.#.....#.#', '###########']
data2 = ['#######', '#S....#', '#####.#', '#E#.#.#', '#.###.#', '#.....#', '#######']

class MazeSolver:
    MOVES = {">": (0, 1), "<":(0,-1), "v":(1,0), "^": (-1,0)}

    def __init__(self, inp_grid):
        grid_dict = defaultdict(str)
        for row_no, row_data in enumerate(inp_grid):
            for col_no, char in enumerate(row_data):
                coord = (row_no, col_no)
                grid_dict[coord] = char
                if char == "S":
                    self.start = coord
                elif char == "E":
                    self.goal = coord
        self.grid_dict = grid_dict

    def print_grid(self, path = []):
        grid_dict = self.grid_dict
        max_row = max(r for r, c in grid_dict)
        max_col = max(c for r, c in grid_dict)
        print_data = []
        for row_no in range(max_row + 1):
            row_data = ""
            for col_no in range(max_col + 1):
                coord = (row_no, col_no)
                if coord in path:
                    use_char = "0"
                else:
                    use_char = grid_dict[coord]
                row_data += use_char
            print_data.append(row_data)
        print("\n".join(print_data))

    def shortest_path(self):
        visited = set(self.start)
        queue = deque([(self.start, 0)])
        while queue:
            pos, steps = queue.popleft()
            if pos == self.goal:
                return steps # assumes first path is shortest path
            for dr, dc in self.MOVES.values():
                npos = pos[0] + dr, pos[1] + dc
                if (npos in self.grid_dict
                        and self.grid_dict[npos] != "#"
                        and npos not in visited):
                    queue.append((npos, steps + 1))
                    visited.add(npos)
        return float("inf")

    def teleportation_path(self):
        visited = {self.start}
        queue = deque([(self.start, 0)])
        while queue:
            pos, steps = queue.popleft()
            if pos == self.goal:
                return steps  # BFS guarantees this is shortest

            for dr, dc in self.MOVES.values():
                # --- Option 1: walk one step ---
                walk_pos = (pos[0] + dr, pos[1] + dc)
                if (walk_pos in self.grid_dict
                        and self.grid_dict[walk_pos] != "#"
                        and walk_pos not in visited):
                    visited.add(walk_pos)
                    queue.append((walk_pos, steps + 1))

                # --- Option 2: teleport to end of corridor ---
                cur = pos
                while True:
                    npos = (cur[0] + dr, cur[1] + dc)
                    if npos not in self.grid_dict or self.grid_dict[npos] == "#":
                        break
                    cur = npos
                if cur != pos and cur not in visited:
                    visited.add(cur)
                    queue.append((cur, steps + 1))

        return float("inf")

    def double_portal_teleportation(self):
        visited = {self.start}
        portals = {"o": {0: (0,0),  1: (0,0)}, "b": {0: (0,0),  1: (0,0)}}
        queue = deque([(self.start, 0, portals)])
        while queue:
            pos, steps, portal = queue.popleft()
            if pos == self.goal:
                return steps  # BFS guarantees this is shortest

            for dr, dc in self.MOVES.values():
                # --- Option 1: walk one step ---
                walk_pos = (pos[0] + dr, pos[1] + dc)
                if (walk_pos in self.grid_dict
                        and self.grid_dict[walk_pos] != "#"
                        and walk_pos not in visited):
                    visited.add(walk_pos)
                    queue.append((walk_pos, steps + 1, portal))

                # --- Option 2: teleport to end of corridor ---
                cur = pos
                while True:
                    npos = (cur[0] + dr, cur[1] + dc)
                    if npos not in self.grid_dict or self.grid_dict[npos] == "#":
                        break
                    cur = npos
                if cur != pos and cur not in visited:
                    visited.add(cur)
                    queue.append((cur, steps + 1, portal))

        return float("inf")

    def double_portal_teleportation(self):
        # portal = (open_tile, wall_tile) or None
        start_state = (self.start, None, None)
        visited = {start_state}
        queue = deque([(self.start, 0, None, None)])
        count = 0
        while queue:
            pos, steps, orange, blue = queue.popleft()
            count += 1
            if count % 50000 == 0:
                print(count, steps)
            if pos == self.goal:
                return steps  # BFS guarantees this is shortest

            for dr, dc in self.MOVES.values():
                npos = (pos[0] + dr, pos[1] + dc)

                # --- Walk ---
                if npos in self.grid_dict and self.grid_dict[npos] != "#":
                    key = (npos, orange, blue)
                    if key not in visited:
                        visited.add(key)
                        queue.append((npos, steps + 1, orange, blue))
                else:
                    # walking "into a wall" - only valid if that wall holds a portal
                    exit_pos = None
                    if orange is not None and orange[1] == npos:
                        exit_pos = blue[0] if blue is not None else None
                    elif blue is not None and blue[1] == npos:
                        exit_pos = orange[0] if orange is not None else None

                    if exit_pos is not None:
                        key = (exit_pos, orange, blue)
                        if key not in visited:
                            visited.add(key)
                            queue.append((exit_pos, steps + 1, orange, blue))

                # --- Shoot a portal in this direction (slide to end of corridor) ---
                cur = pos
                while True:
                    probe = (cur[0] + dr, cur[1] + dc)
                    if probe not in self.grid_dict or self.grid_dict[probe] == "#":
                        break
                    cur = probe
                wall_tile = (cur[0] + dr, cur[1] + dc)

                # only a real interior wall can hold a portal, not the map edge
                if wall_tile in self.grid_dict and self.grid_dict[wall_tile] == "#":
                    new_portal = (cur, wall_tile)

                    # shoot orange
                    key_o = (pos, new_portal, blue)
                    if key_o not in visited:
                        visited.add(key_o)
                        queue.append((pos, steps + 1, new_portal, blue))

                    # shoot blue
                    key_b = (pos, orange, new_portal)
                    if key_b not in visited:
                        visited.add(key_b)
                        queue.append((pos, steps + 1, orange, new_portal))

        return float("inf")

maze = MazeSolver(data)
print("FlipFlop 2026, Puzzle 09")
print("Part 1:", maze.shortest_path())
print("Part 2:", maze.teleportation_path())
# print("Part 3:", maze.double_portal_teleportation())

print("Part 3:", "SOLVED, NEED TO IMPROVE SPEED")