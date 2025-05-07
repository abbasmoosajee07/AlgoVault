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

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    instructions = input_data[0].split('\n')
    directions = input_data[1].split('\n')[0]

class MindCube:
    def __init__(self, cube_faces: list[str], size: tuple):
        self.instructions = self.parse_input(cube_faces)
        cube_faces = {}
        for face in range(1, 6 + 1):
            cube_faces[face] = {(row, col): 1
                                for row in range(1, size[0] + 1)
                                for col in range(1, size[1] + 1)}
        self.cube_faces = cube_faces
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

    @staticmethod
    def check_value(base_value: int):
        while base_value > 100:
            base_value -= 100
        while base_value < 0:
            base_value += 100
        return base_value

    def get_adjacent_face(self, twist: str, cube: dict):
        # Define face rotation orders for each twist direction
        rotations = {
            "L": ["C", "L", "O", "R"],
            "R": ["C", "R", "O", "L"],
            "U": ["C", "U", "O", "D"],
            "D": ["C", "D", "O", "U"],
        }

        new_cube = cube.copy()
        if twist in rotations:
            keys = rotations[twist]
            values = [cube[k] for k in keys]
            # Rotate values one step to the left
            for i, k in enumerate(keys):
                new_cube[k] = values[(i + 1) % len(values)]

        return new_cube

    def perform_transformations(self, twists):
        cube_dict = {"C": 1, "L": 5, "R": 6, "U": 4, "D": 2, "O": 3}
        current_face = cube_dict["C"]
        absorptions = {}
        cube_faces = self.cube_faces.copy()

        for idx, instruc in enumerate(self.instructions):
            face_data = cube_faces[current_face]
            updated_face = face_data.copy()
            op_type = instruc[0]

            if op_type == "FACE":
                delta = instruc[1]
                for pos in face_data:
                    updated_face[pos] = self.check_value(face_data[pos] + delta)
                power = delta * self.CUBE_SIZE[0] * self.CUBE_SIZE[1]

            elif op_type == "ROW":
                row, delta = instruc[1], instruc[2]
                for pos in face_data:
                    if pos[0] == row:
                        updated_face[pos] = self.check_value(face_data[pos] + delta)
                power = delta * self.CUBE_SIZE[0]

            elif op_type == "COL":
                col, delta = instruc[1], instruc[2]
                for pos in face_data:
                    if pos[1] == col:
                        updated_face[pos] = self.check_value(face_data[pos] + delta)
                power = delta * self.CUBE_SIZE[1]

            cube_faces[current_face] = updated_face
            absorptions[current_face] = absorptions.get(current_face, 0) + power

            # Apply twist if available
            if idx < len(twists):
                twist_dir = twists[idx]
                cube_dict = self.get_adjacent_face(twist_dir, cube_dict)
                current_face = cube_dict["C"]

        return absorptions


cubes = MindCube(instructions, (80, 80))

absorption = cubes.perform_transformations(directions)
print("Part 1:", np.prod(sorted(absorption.values(), reverse=True)[:2]))

print(f"Execution Time = {time.time() - start_time:.5f}s")

# The first instruction, ‘FACE - VALUE 38’, is performed on face 1. On a 3 by 3 grid, this instruction has a power of 342. Hence, face 1 now has a total absorption of 342.
# Then, the twist “L” is performed, and the ‘current face’ changes to face 5. The orientation has changed due to the twist. At this stage, face 4 is above, face 1 is to the right, face 2 is below, and face 3 is to the left.
# The second instruction, ‘ROW 2 - VALUE 71’, has a power of 213 and is performed on face 5. Hence, face 5 now has a total absorption of 213.
# The twist “U” is performed, and the ‘current face’ changes to face 4.
# The third instruction, ‘ROW 1 - VALUE 57’, has a power of 171 and is performed on face 4. Hence, face 4 now has a total absorption of 171.
# The twist “R” is performed, and the ‘current face’ changes to face 1.
# The fourth instruction, ‘ROW 3 - VALUE 68’, has a power of 204 and is performed on face 1. Hence, face 1 now has a total absorption of 546.
# The twist “D” is performed, and the ‘current face’ changes to face 5.
# The final instruction, ‘COL 1 - VALUE 52’, has a power of 156 and is performed on face 5. Hence, face 5 now has a total absorption of 369.
# After all the instructions were performed, the two highest total absorptions were 546 (face 1) and 369 (face 5). The product of these absorptions is 546 x 369 = 201474. Hence, the answer for this file is 201474.
