"""Eldarverse Puzzles - Problem F
Solution Started: September 4,
Puzzle Link: https://www.eldarverse.com/problem/sep-25-long-F
Solution by: Abbas Moosajee
Brief: [Bases and Plants]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "problem-sep-25-long-F-input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
    data1  = ['2', '3 3 3', 'M..', '...', '...', '5 3 7', '..X', 'X.X', 'M..', '...', '.XX']


def parse_raw_data(raw_data):
    test_cases = []
    new_test = True
    for line_no, line_data in enumerate(raw_data[1:], start = 1):
        if new_test:
            test_data = tuple(map(int, line_data.split(" ")))
            map_data = ""
            target_line = line_no + test_data[0]
            new_test = False
        elif line_no <= target_line:
            map_data += f"{line_data}\n"
            if line_no == target_line:
                test_cases.append([test_data, map_data])
                new_test = True
    return test_cases

class StrategyGame:
    def __init__(self, map_props, map_data):
        self.N, self.M, self.K = map_props
        self.map_data = map_data
        self.buildable = self._parse_map(map_data.splitlines())

    def _parse_map(self, map_data):
        self.map_dict = {}
        buildable = set()
        for i, row_data in enumerate(map_data):
            for j, cell in enumerate(row_data):
                self.map_dict[(i, j)] = cell
                if cell == "M":
                    self.missile = (i, j)
                elif cell == ".":
                    buildable.add((i, j))
        return buildable

    def print_map(self, build_sites):
        rows = max(i for i, _ in self.map_dict) + 1
        cols = max(j for _, j in self.map_dict) + 1
        lines = []
        for i in range(rows):
            row_data = ""
            for j in range(cols):
                if (i, j) in build_sites:
                    row_data += build_sites[(i, j)]
                else:
                    row_data += self.map_dict[(i, j)]
            lines.append(row_data)
        return "\n".join(lines)

    def __calc_missile_fuel(self, i, j):
        X, Y = self.missile
        return (X - i)**2 + (Y - j)**2

    def get_optimal_solution(self):
        # 1) gather all buildable cells and their squared distances
        cells = []
        for (i, j) in self.buildable:
            d = self.__calc_missile_fuel(i, j)
            cells.append(((i, j), d))

        # sanity
        if len(cells) < self.K:
            raise ValueError("not enough buildable cells")

        # 2) pick the K farthest cells (positions + weights)
        cells.sort(key=lambda x: x[1], reverse=True)
        chosen = cells[:self.K]               # list of ((i,j), d)
        positions = [pos for pos, d in chosen]
        weights = [d for pos, d in chosen]
        total = sum(weights)

        # Edge case: if K == 1, you cannot have both types -> min cost is 0.
        if self.K == 1:
            build_dict = {positions[0]: "B"}
            return 0, self.print_map(build_dict) + "\n"

        # 3) subset-sum DP (bitset) to find achievable subset sums using the K items
        # dp_prefix[i] = int bitset of sums achievable using items 0..i-1
        dp_prefix = [0] * (self.K + 1)
        dp_prefix[0] = 1  # bit 0 set
        for i, w in enumerate(weights):
            dp_prefix[i+1] = dp_prefix[i] | (dp_prefix[i] << w)

        # 4) find best s <= total//2, but also ensure non-empty both groups:
        half = total // 2
        all_sums_bitset = dp_prefix[self.K]
        # mask lower half (0..half)
        mask = all_sums_bitset & ((1 << (half + 1)) - 1)
        if mask == 0:
            # no subset sum <= half (shouldn't happen), fallback to 0
            best_s = 0
        else:
            # highest set bit in mask is the best s <= half
            best_s = mask.bit_length() - 1

        # Ensure both groups non-empty (subset not zero and not full set)
        # If best_s == 0 or best_s == total, try next smaller achievable s > 0.
        if best_s == 0:
            # remove bit 0 and search again (we need non-empty)
            mask_no_zero = mask & ~1
            if mask_no_zero != 0:
                best_s = mask_no_zero.bit_length() - 1
            else:
                # no non-empty subset <= half: must force some assignment (rare; happens when K==1)
                best_s = 0

        # 5) backtrack to find which items produce sum = best_s
        chosen_indices_in_A = [False] * self.K
        s = best_s
        for i in range(self.K - 1, -1, -1):
            # if sum s is achievable without item i (i.e. from dp_prefix[i]), then item i not taken
            if (dp_prefix[i] >> s) & 1:
                # not taken
                continue
            else:
                # must have taken item i
                chosen_indices_in_A[i] = True
                s -= weights[i]

        # compute sums for verification
        sumA = sum(weights[i] for i in range(self.K) if chosen_indices_in_A[i])
        sumB = total - sumA
        best_value = min(sumA, sumB)

        # 6) assign letters and build map
        build_dict = {}
        # put group A as 'B' (bases) and group B as 'E' (plants)
        for idx, pos in enumerate(positions):
            build_dict[pos] = "B" if chosen_indices_in_A[idx] else "E"

        # final map string
        new_map = self.print_map(build_dict)
        return best_value, new_map + "\n"

solutions = []
test_cases = parse_raw_data(data)

for case_no, case_data in enumerate(test_cases, start=1):
    map_props, map_data = case_data
    case_game = StrategyGame(map_props, map_data)
    energy, opt_map = case_game.get_optimal_solution()
    case_soln = f"Case #{case_no}: {energy}\n{opt_map}"
    solutions.append(case_soln)
    print(solutions[-1])


output_file = "problem-sep-25-long-F-output.txt"
output_path = Path(__file__).parent / output_file
with output_path.open("w", encoding="utf-8") as f:
    f.write("".join(solutions))
