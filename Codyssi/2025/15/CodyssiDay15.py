"""Codyssi Puzzles - Problem 15
Solution Started: Apr 27, 2025
Puzzle Link: https://www.codyssi.com/view_problem_19?
Solution by: Abbas Moosajee
Brief: [Artifacts at Atlantis]
"""

#!/usr/bin/env python3

import os, re, copy, time
start_time = time.time()

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    artifact_dict = {nam: int(val) for idx, line in enumerate(input_data[0].split('\n') )for nam, val in [line.split(' | ')]}
    artifact_check = [(nam, int(val)) for line in input_data[1].split('\n') for nam, val in [line.split(' | ')]]

class Archaeologist:
    def __init__(self, artifacts: list[tuple]):
        self.artifact_dict = artifacts

    def __compare_nodes(self, art_code, root_code, layer, path):
        id_val = self.artifact_dict[art_code]
        root_id = self.artifact_dict[root_code]

        direction = "left" if id_val < root_id else "right" if id_val > root_id else None
        new_path = path + [root_code]

        if direction:
            if not self.branch_network[root_code][direction]:
                # Insert new node
                self.branch_network[root_code][direction].append(art_code)
                self.branch_network[art_code] = {"left": [], "right": []}
                self.tree_layers.setdefault(layer + 1, []).append(self.artifact_dict[art_code])
                return new_path + [art_code]
            else:
                # Recurse to next level and return full path
                child_code = self.branch_network[root_code][direction][0]
                return self.__compare_nodes(art_code, child_code, layer + 1, new_path)
        else:
            # Equal ID value case
            if art_code not in self.branch_network:
                self.branch_network[art_code] = {"left": [], "right": []}
                self.tree_layers.setdefault(layer, []).append(self.artifact_dict[art_code])
            return new_path + [art_code]

    def build_tree(self):
        root_node = next(iter(self.artifact_dict))
        self.branch_network = {}
        self.artifact_paths = {}
        self.tree_layers = {}
        for artifact in self.artifact_dict.keys():
            path = self.__compare_nodes(artifact, root_node, 1, [])
            self.artifact_paths[artifact] = path
        return self.tree_layers

    def place_artifact(self, new_id):
        self.artifact_dict["new"] = new_id
        path = self.__compare_nodes("new", next(iter(self.artifact_dict)), 1, [])
        return path

    def find_common_ancestor(self, check_artifacts):
        path_1 = self.artifact_paths[check_artifacts[0][0]]
        path_2 = self.artifact_paths[check_artifacts[1][0]]
        lca = None
        for a, b in zip(path_1, path_2):
            if a == b:
                lca = a
        return lca

expedition = Archaeologist(artifact_dict)

layered_tree = expedition.build_tree()
layer_sum = [sum(branch) for branch in layered_tree.values()]
print("Part 1:", len(layered_tree) * max(layer_sum))

artifact_path = expedition.place_artifact(500000)
print("Part 2:", '-'.join(artifact_path[:-1]))

common_artifact = expedition.find_common_ancestor(artifact_check)
print("Part 3:", common_artifact)

# print(f"Execution Time = {time.time() - start_time:.5f}s")

