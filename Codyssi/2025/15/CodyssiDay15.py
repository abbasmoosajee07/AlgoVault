"""Codyssi Puzzles - Problem 15
Solution Started: Apr 27, 2025
Puzzle Link: https://www.codyssi.com/view_problem_19?
Solution by: Abbas Moosajee
Brief: [Artifacts at Atlantis]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D15_file = "Day15_input1.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    artifact_dict = {nam: int(val) for idx, line in enumerate(input_data[0].split('\n') )for nam, val in [line.split(' | ')]}
    artifact_list1 = [(nam, int(val)) for line in input_data[1].split('\n') for nam, val in [line.split(' | ')]]

class Archaeologist:
    def __init__(self, artifacts: list[tuple]):
        self.artifact_dict = artifacts

    def __compare_nodes(self, art_code, root_code, layer):
        id_val = self.artifact_dict[art_code]
        root_id = self.artifact_dict[root_code]

        direction = "left" if id_val < root_id else "right" if id_val > root_id else None

        if direction:
            if not self.branch_network[root_code][direction]:
                # Insert new node
                self.branch_network[root_code][direction].append(art_code)
                self.branch_network[art_code] = {"left": [], "right": []}
                self.tree_layers.setdefault(layer + 1, []).append(self.artifact_dict[art_code])
            else:
                # Recurse to next level
                child_code = self.branch_network[root_code][direction][0]
                self.__compare_nodes(art_code, child_code, layer + 1)
        else:
            # Equal ID value, insert at current level if not already present
            if art_code not in self.branch_network:
                self.branch_network[art_code] = {"left": [], "right": []}
                self.tree_layers.setdefault(layer, []).append(self.artifact_dict[art_code])

    def build_tree(self):
        root_node = next(iter(self.artifact_dict))
        self.branch_network = {}
        self.tree_layers = {}
        for artifact in self.artifact_dict.keys():
            self.__compare_nodes(artifact, root_node, 1)

        layer_sum = [sum(branch) for branch in self.tree_layers.values()]
        return len(self.tree_layers) * max(layer_sum)

expedition = Archaeologist(artifact_dict)

layered_tree = expedition.build_tree()
print("Part 1:", layered_tree)

print(f"Execution Time = {time.time() - start_time:.5f}s")

