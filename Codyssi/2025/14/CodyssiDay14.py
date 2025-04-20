"""Codyssi Puzzles - Problem 14
Solution Started: Apr 18, 2025
Puzzle Link: https://www.codyssi.com/view_problem_18?
Solution by: Abbas Moosajee
Brief: [Crucial Crafting]
"""

#!/usr/bin/env python3

import os, re, copy, itertools, time, heapq
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

    def validate_combo(self, combo_materials: list[str], avail_cost: int):
        synth_items = np.array([self.items_dict[mat] for mat in combo_materials])
        total_qlty = sum(synth_items[:,0])
        total_cost = sum(synth_items[:,1])
        reqd_mats = sum(synth_items[:,2])
        if total_cost <= avail_cost:
            # print(total_qlty, reqd_mats, total_cost)
            return (total_qlty, reqd_mats)
        else:
            return (0, 0)

    def optimal_combinations(self, spend_units: int):

        items = self.items_dict
        elements = list(items.keys())
        top_k = 50
        heap = []
        current_combinations = []

        # for num in range(2, 15):
        #     for pair in itertools.combinations(elements, num):
        #         quality, unique = self.validate_combo(pair, spend_units)
        #         score = quality * unique
        #         if len(heap) < top_k:
        #             heapq.heappush(heap, (score, pair))
        #         else:
        #             heapq.heappushpop(heap, (score, pair))

        # def score_pair(pair):
        #     quality, unique = self.validate_combo(pair, spend_units)
        #     return quality * unique

        # with ThreadPoolExecutor() as executor:
        #     for num in range(2, 10):
        #         groupings = itertools.combinations(elements, num)
        #         current_combinations.extend(executor.map(score_pair, groupings))

        return current_combinations

synth = Synthesiser(input_data)

ranked_items = synth.count_unique_materials()
print("Part 1:", sum(ranked_items[-5:,2]))

opt_materials = synth.optimal_combinations(30)
print("Part 2:", max(opt_materials))

print(f"Execution Time = {time.time() - start_time:.5f}s")
