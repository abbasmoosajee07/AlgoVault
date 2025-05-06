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
D16_file = "Day16_input1.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    cube_faces = input_data[0].split('\n')
    directions = input_data[1].split('\n')[0]

class MindCube:
    def __init__(self, cube_faces: list[str], size: tuple):
        self.CUBE_SIZE = size
        self.cube_face = self.parse_input(cube_faces)
        self.base_cube = {(face, row, col): 1 for face in range(1, size[0] + 1)
                        for row in range(size[1]) for col in range(size[2])}

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

    def get_adjacent_face(self, current: int, twist: str):
        
        faces_dict = {
            1:{"L":5, "R":6, "U":4, "D":2},
            2:{"L":5, "R":6, "U":1, "D":3},
            3:{"L":5, "R":6, "U":2, "D":4},
            4:{"L":5, "R":6, "U":3, "D":1},
            5:{"L":3, "R":1, "U":4, "D":2},
            6:{"L":1, "R":3, "U":4, "D":2},
        }
            #   1
            #  526
            #   3
            #   4

        new_face = faces_dict[current][twist]
        return new_face

    def perform_transformations(self, instructions):
        current_face = 1
        # for line in self.cube_face:
        #     if line[0] == "FACE":
        #         for row in range(self.CUBE_SIZE[1]):
        #             for col in range(self.CUBE_SIZE[2]):
        #                 self.base_cube[(current_face, row, col)] = line[1]
        # print(self.base_cube)
        for twist_dir in instructions:
            twist_face = self.get_adjacent_face(current_face, twist_dir)
            print(f"{twist_dir}: {current_face} -> {twist_face}")
            current_face = twist_face
        return len(self.base_cube)

cubes = MindCube(cube_faces, (6, 80, 80))

absorption = cubes.perform_transformations(directions)
print("Part 1:", absorption)

print(f"Execution Time = {time.time() - start_time:.5f}s")


# The twist “L” is performed, the ‘current face’ changes to face 5. The orientation has changed due to the twist. At this stage, face 4 is above, face 1 is to the right, face 2 is below, and face 3 is to the left.
# The twist “U” is performed, the ‘current face’ changes to face 4.
# The twist “R” is performed, the ‘current face’ changes to face 1.
# The twist “D” is performed, the ‘current face’ changes to face 5.
