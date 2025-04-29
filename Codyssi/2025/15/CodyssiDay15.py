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
    artifact_list = [(nam, int(val)) for idx, line in enumerate(input_data[0].split('\n') )for nam, val in [line.split(' | ')]]
    artifact_list1 = [(nam, int(val)) for line in input_data[1].split('\n') for nam, val in [line.split(' | ')]]

class Archaeologist:
    def __init__(self, artifacts: list[tuple]):
        self.artifact_list = artifacts
        self.artifact_dict = {val: name for name, val in artifacts}

    def __compare_nodes(self, artifact, root_node, layer):
        code, id_val = artifact
        print(self.tree)
        if id_val < root_node[1]:
            print("left", code, id_val)
            # if 
            self.tree[root_node[0]]["left"].append(code)
        elif id_val > root_node[1]:
            print("right", code, id_val)
        else:
            self.tree[code] = {"left": [], "right": []}
            print(code, id_val)
        return

    def build_tree(self):
        root_node = self.artifact_list[0]
        self.tree = {}
        for artifact in self.artifact_list[:2]:
            self.__compare_nodes(artifact, root_node, 1)
        print(self.tree)
        return len(self.tree)

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
