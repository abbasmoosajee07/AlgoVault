"""Codyssi Puzzles - Problem 16
Solution Started: Apr 30, 2025
Puzzle Link: https://www.codyssi.com/view_problem_20?
Solution by: Abbas Moosajee
Brief: [Leviathan Mindscape]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    cube_faces = input_data[0].split('\n')
    directions = input_data[1].split('\n')[0]

class MindCube:
    def __init__(self, cube_faces: list[str]):
        cube_list = self.parse_input(cube_faces)
        print(cube_list)
    @staticmethod
    def parse_input(input_faces):
        cube_list = []
        for line in input_faces:
            parts = line.split()
            if parts[0] == "FACE":
                cube_list.append(("FACE", int(parts[-1])))
            else:
                cube_list.append((parts[0], int(parts[1]), int(parts[-1])))
        return cube_list

cubes = MindCube(cube_faces)