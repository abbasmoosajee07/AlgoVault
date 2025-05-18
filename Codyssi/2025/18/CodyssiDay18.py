"""Codyssi Puzzles - Problem 18
Solution Started: May 17, 2025
Puzzle Link: https://www.codyssi.com/view_problem_22?
Solution by: Abbas Moosajee
Brief: [Cataclysmic Escape]
"""

#!/usr/bin/env python3

import os, re, copy, time
from itertools import product
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')
    feasible_spaces = {"Day18_input1.txt":(10, 15, 60, 3), "Day18_input2.txt":(3,3,5,3),
        "Day18_input.txt":(10, 15, 60, 3), "Day18_input3.txt":(10, 15, 60, 3)}
    feasible = feasible_spaces[D18_file]

class Submarine:
    def __init__(self, all_rules, feasible_space):
        self.feasible_space = feasible_space
        self.rule_dict = {}
        for rule in all_rules:
            self.parse_rules(rule)
        MIN_LIMITS = (0, 0, 0, -1)
        self.space_region = {
            "x" : range(MIN_LIMITS[0], feasible_space[0]),
            "y" : range(MIN_LIMITS[1], feasible_space[1]),
            "z" : range(MIN_LIMITS[2], feasible_space[2]),
            "a" : range(MIN_LIMITS[3], feasible_space[3] -1)
        }
        self.all_coords = list(product(self.space_region['x'], self.space_region['y'], \
                                self.space_region['z'], self.space_region['a']))

    def parse_rules(self, rule):

        # Split rule into rule number and description
        rule_no_str, info = rule.split(': ', 1)
        rule_no = int(rule_no_str.strip("RULE "))

        # Regex to extract coefficients and velocity
        pattern = (
            r"(\d+)x\+(\d+)y\+(\d+)z\+(\d+)a DIVIDE (\d+) HAS REMAINDER (\d+)"
            r" \| DEBRIS VELOCITY \((-?\d+), (-?\d+), (-?\d+), (-?\d+)\)"
        )

        match = re.match(pattern, info)
        values = list(map(int, match.groups()))

        # Build parsed dictionary
        parsed_data = {
            "x": values[0], "y": values[1], "z": values[2], "a": values[3],
            "div": values[4], "rem": values[5],
            "vx": values[6], "vy": values[7], "vz": values[8], "va": values[9],
        }

        # Store in rule_dict
        self.rule_dict[rule_no] = parsed_data

    def __check_debris(self, coords, rule_no):
        rule_check = self.rule_dict[rule_no]
        debris_total = (
            (rule_check['x'] * coords[0]) + (rule_check['y'] * coords[1]) +\
            (rule_check['z'] * coords[2]) + (rule_check['a'] * coords[3])
            )
        if (debris_total % rule_check["div"]) == rule_check["rem"]:
            return True
        else:
            return False

    def count_debris(self):
        debris_dict = {}
        count = 0
        for coords in self.all_coords:
            for rule in self.rule_dict:
                check = self.__check_debris(coords, rule)
                if check:
                    count += 1
                    debris_dict.setdefault(rule, set()).add(coords)
        # total_debris = {rule: len(debris) for rule, debris in debris_dict.items()}
        return count

sub = Submarine(input_data, feasible)

debris = sub.count_debris()
print("Part 1:", debris)

print(f"Execution Time = {time.time() - start_time:.5f}s")
