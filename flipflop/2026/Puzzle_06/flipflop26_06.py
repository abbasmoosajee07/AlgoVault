"""FlipFlop 2026: BitFlop Internship - Puzzle 6
Solution Started: July 22, 2026
Puzzle Link: https://flipflop.slome.org/2026/6
Solution by: Abbas Moosajee
Brief: [Gears and lights]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
import string

# Load input file
input_file = "puzzle_06_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class GearBox:
    DIRS = {">": (0, 1), "<":(0,-1), "v":(1,0), "^": (-1,0)}
    def __init__(self, raw_data):
        self.size = len(raw_data), len(raw_data[0])
        self.raw_data = raw_data
        self.start_turn = "L"

    @staticmethod
    def parse_grid(data, valid = ''):
        grid_dict, rev_dict = defaultdict(str), defaultdict(list)
        for row_no, row in enumerate(data):
            for col_no, char in enumerate(row):
                if char in valid:
                    grid_dict[(row_no, col_no)] = char
                    rev_dict[char].append((row_no, col_no))
        return grid_dict, rev_dict

    def print_grid(self, grid_dict):
        max_row, max_col = self.size
        print_data = []
        for row_no in range(max_row):
            row_data = ""
            for col_no in range(max_col):
                coord = (row_no, col_no)
                row_data += grid_dict.get(coord, ".")
            print_data.append(row_data)
        print("\n".join(print_data))

    @staticmethod
    def bin_to_dec(bin_str):
        if len(bin_str) <= 0:
            return("Empty Str")
        return int(bin_str, 2)

    @staticmethod
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def check_prime_gears(self, grid_dict, rev_dict, valid_gears):
        gear_primes = defaultdict(int)
        for prime_name in string.ascii_uppercase:
            if prime_name not in rev_dict:
                continue
            visited = set()
            check_queue = list(rev_dict[prime_name])
            while check_queue:
                pos = check_queue.pop()
                for dr, dc in self.DIRS.values():
                    npos = (pos[0] + dr, pos[1] + dc)
                    if npos in visited:
                        continue
                    component = grid_dict.get(npos)
                    if component in valid_gears:
                        visited.add(npos)
                        gear_primes[prime_name] += 1
                        check_queue.append(npos)
        return gear_primes

    def find_light_code(self, grid_dict, rev_dict):
        bin_str = ""
        all_lights = sorted(rev_dict["*"], reverse=True)
        while all_lights:
            check_light = all_lights.pop()
            for dr, dc in self.DIRS.values():
                npos = check_light[0] + dr, check_light[1] + dc
                status = grid_dict.get(npos)
                if status in ("L","R"):
                    light_status = "0" if status == "L" else "1"
                    bin_str += light_status
                    grid_dict[check_light] = light_status
        return self.bin_to_dec(bin_str)

    def identify_lights(self, with_bluetooth = False, with_prime = False):
        if with_bluetooth:
            valid_components = string.ascii_letters + "#3*S"
            valid_gears = ("#", "3")
        else:
            valid_components = "#*S"
            valid_gears = ("#", )

        grid_dict, rev_dict = self.parse_grid(self.raw_data, valid_components)
        if with_prime:
            prime_gears = self.check_prime_gears(grid_dict, rev_dict, valid_gears)
        else:
            prime_gears = defaultdict(int)

        def mark_and_queue(origin, ndir, queue):
            for dr, dc in self.DIRS.values():
                npos = (origin[0] + dr, origin[1] + dc)
                if grid_dict.get(npos) in valid_gears:
                    grid_dict[npos] = ndir
                    queue.append((npos, ndir))

        queue = deque([(rev_dict["S"][0], self.start_turn)])
        while queue:
            pos, turn = queue.popleft()
            ndir = "R" if turn == "L" else "L"
            for dr, dc in self.DIRS.values():
                npos = (pos[0] + dr, pos[1] + dc)
                component = grid_dict.get(npos)
                if component in valid_gears:
                    grid_dict[npos] = ndir
                    queue.append((npos, ndir))
                elif component and component in string.ascii_lowercase:
                    if with_prime and self.is_prime(prime_gears[component.upper()]) is True:
                        continue
                    portal_out = rev_dict[component.upper()][0]
                    mark_and_queue(portal_out, ndir, queue)
        return self.find_light_code(grid_dict, rev_dict)

gears = GearBox(data)
print("FlipFlops 2026, Puzzle 06")
print("Part 1:", gears.identify_lights())
print("Part 2:", gears.identify_lights(with_bluetooth=True))
print("Part 3:", gears.identify_lights(with_bluetooth=True, with_prime=True))
