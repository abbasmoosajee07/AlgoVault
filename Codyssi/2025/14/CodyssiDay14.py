"""Codyssi Puzzles - Problem 14
Solution Started: Apr 18, 2025
Puzzle Link: https://www.codyssi.com/view_problem_18?
Solution by: Abbas Moosajee
Brief: [Crucial Crafting]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
start_time = time.time()

# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')

class Synthesiser:
    def __init__(self, item_list: list[str]):
        self.parse_input(item_list)

    def parse_input(self, item_list: list[str]):
        """
        Creates a dict ofr each material with a tuple of properties,
        `Quality, Cost and Unique Materials` values
        """
        item_info = r"(\d+)\s+(\w+)\s+\|\s+Quality\s*:\s*(\d+),\s*Cost\s*:\s*(\d+),\s*Unique Materials\s*:\s*(\d+)"
        items_dict = {}
        for item in item_list:
            match = re.search(item_info, item)
            props_list = list(match.groups())
            items_dict[props_list[1]] = tuple(map(int, props_list[2:]))
        self.items_dict = items_dict

    def count_unique_materials(self):
        items_array = np.array(list(self.items_dict.values()))
        sorted_items = sorted(items_array, key=lambda row: (row[0], row[1]))
        return np.array(sorted_items)

    def optimal_combinations(self, spend_units: int):
        """
        Dynamic programming to find best combination within spend_units
        """
        dp = [(-1, float('inf'))] * (spend_units + 1)  # (quality, unique_materials)
        dp[0] = (0, 0)  # base case: 0 cost, 0 quality, 0 materials

        for (quality, cost, unique) in self.items_dict.values():
            for c in range(spend_units, cost - 1, -1):
                prev_quality, prev_unique = dp[c - cost]
                if prev_quality != -1:  # only proceed if previous state is valid
                    new_quality = prev_quality + quality
                    new_unique = prev_unique + unique
                    if (new_quality > dp[c][0]) or \
                        (new_quality == dp[c][0] and new_unique < dp[c][1]):
                        dp[c] = (new_quality, new_unique)

        # Find the best result across all dp[cost] where cost <= spend_units
        best_quality, best_unique = max(dp, key=lambda x: (x[0], -x[1]))

        if best_quality <= 0:
            return 0  # no valid combination

        return best_quality * best_unique
synth = Synthesiser(input_data)

ranked_items = synth.count_unique_materials()
print("Part 1:", sum(ranked_items[-5:,2]))

opt_materials_30 = synth.optimal_combinations(30)
print("Part 2:", opt_materials_30)

opt_materials_300 = synth.optimal_combinations(300)
print("Part 3:", opt_materials_300)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
