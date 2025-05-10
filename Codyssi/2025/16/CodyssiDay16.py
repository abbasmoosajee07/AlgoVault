"""Codyssi Puzzles - Problem 16
Solution Started: Apr 30, 2025
Puzzle Link: https://www.codyssi.com/view_problem_20?
Solution by: Abbas Moosajee
Brief: [Leviathan Mindscape]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)
cube_size = (3, 3) if D16_file == "Day16_input1.txt" else (80, 80)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    instructions = input_data[0].split('\n')
    directions = input_data[1].split('\n')[0]

class MindCube:
    def __init__(self, cube_faces: list[str], size: tuple):
        faces, cube_dict = [{}, {}]
        for index, coords in enumerate(['x','y','z','-x','-y','-z'], start = 0):
            faces[coords] = np.full((size[0], size[1]), 1, dtype=object)
            cube_dict[coords] = index

        self.cube_faces, self.cube_dict = faces, cube_dict
        self.instructions = self.parse_input(cube_faces)
        self.CUBE_SIZE = size

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

    def rotate(self, twist, cube_faces, cube_dict):
        def self_rotate(face, num):
            for _ in range(num):
                face = np.rot90(face)
            return face

        orientations = {
            'L': {'x':['-y',0],'-y':['-x',0],'-x':['y',0],'y':['x',0],'z':['z',1],'-z':['-z',3]},
            'R': {'x':['y',0],'y':['-x',0],'-x':['-y',0],'-y':['x',0],'z':['z',3],'-z':['-z',1]},
            'D': {'y':['z',0],'z':['-y',2],'-y':['-z',0],'-z':['y',2],'x':['x',3],'-x':['-x',1]},
            'U': {'y':['-z',2],'-z':['-y',0],'-y':['z',2],'z':['y',0],'x':['x',1],'-x':['-x',3]}
        }
        rotate_dict = orientations[twist]
        cube_faces = {k: self_rotate(cube_faces[v[0]], v[1]) for k, v in rotate_dict.items()}
        cube_dict = {k: cube_dict[rotate_dict[k][0]] if k in rotate_dict else v for k, v in cube_dict.items()}

        return cube_faces, cube_dict

    def perform_transformations(self, twist_list: str):
        cube_dict = self.cube_dict.copy()
        cube_faces = self.cube_faces.copy()
        absorptions = {face:0 for face in cube_dict.values()}
        main_face = 'y'

        for (idx, instruc) in enumerate(self.instructions):
            op_type, delta = instruc[0], instruc[-1]
            current_face = cube_dict[main_face]

            if op_type == "FACE":
                cube_faces[main_face] = (cube_faces[main_face] + instruc[1] - 1) % 100 + 1
                power = delta * self.CUBE_SIZE[0] * self.CUBE_SIZE[1]
            elif op_type == "ROW":
                row_no = instruc[1]
                cube_faces[main_face][row_no - 1, :] = (cube_faces[main_face][row_no- 1, :] + delta - 1) % 100 + 1
                power = delta * self.CUBE_SIZE[0]
            elif op_type == "COL":
                col_no = instruc[1]
                cube_faces[main_face][:,col_no - 1] = (cube_faces[main_face][:,col_no - 1] + delta - 1) % 100 + 1
                power = delta * self.CUBE_SIZE[1]

            absorptions[current_face] += power

            # Apply twist if available
            if idx < len(twist_list):
                twist_dir = twist_list[idx]
                cube_faces, cube_dict = self.rotate(twist_dir, cube_faces, cube_dict)

        return absorptions, cube_faces

    def calculate_dominant_sums(self, cube_faces):
        dominant_faces = []
        for face in cube_faces.values():
            rowmax = [sum(row) for row in face]
            colmax = [sum(row) for row in np.rot90(face)]
            dominant_faces.append(max(max(rowmax), max(colmax)))
        result = 1
        for num in dominant_faces:
            result *= num
        return result

cubes = MindCube(instructions, cube_size)

absorption, final_cube = cubes.perform_transformations(directions)
print("Part 1:", np.prod(sorted(absorption.values(), reverse=True)[:2]))

dominant_sum = cubes.calculate_dominant_sums(final_cube)
print("Part 2:", dominant_sum) # 369594451623936000000

print(f"Execution Time = {time.time() - start_time:.5f}s")
