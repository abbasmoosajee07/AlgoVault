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
    artifact_list = [(idx, nam, int(val)) for idx, line in enumerate(input_data[0].split('\n') )for nam, val in [line.split(' | ')]]
    artifact_list1 = [(nam, int(val)) for line in input_data[1].split('\n') for nam, val in [line.split(' | ')]]

class Archaeologist:
    def __init__(self, artifacts: list[tuple]):
        self.artifacts = artifacts
        self.artifact_dict = {val: name for _, name, val in artifacts}

    def build_tree(self):
        tracked_artifacts = self.artifacts
        tree = {}
        root_node = self.artifacts[0]
        layer = 0
        while tracked_artifacts:
            idx, code, id_value = tracked_artifacts.pop(0)
            print(idx, code, id_value)
            if id_value < root_node[2]:
                layer += 1
                tree.setdefault(layer, []).append(id_value)
            elif id_value > root_node[2]:
                layer -= 1
                tree.setdefault(layer, []).append(id_value)
        print(tree)
        return 1

expedition = Archaeologist(artifact_list)

layered_tree = expedition.build_tree()
print("Part 1:", layered_tree)

print(f"Execution Time = {time.time() - start_time:.5f}s")


# There are 15 artifacts in this list (the last two lines are ignored).
# The first layer of the storage system will hold 1 artifact (ID 576690).
# The second layer of the storage system will hold 2 artifacts (IDs 323352 and 747973).
# The third layer of the storage system will hold 4 artifacts (IDs 55528, 422646, 661714, and 967749).
# The fourth layer of the storage system will hold 4 artifacts (IDs 9047, 200543, 548306, and 960026).
# The fifth layer of the storage system will hold 3 artifacts (IDs 314969, 493637, and 833936).
# The sixth layer of the storage system will hold 1 artifact (ID 499862).
