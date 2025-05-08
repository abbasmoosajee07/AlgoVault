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
D16_file = "Day16_input2.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)
cube_size = (3, 3) if D16_file == "Day16_input1.txt" else (80, 80)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    instructions = input_data[0].split('\n')
    directions = input_data[1].split('\n')[0]

class MindCube:
    def __init__(self, cube_faces: list[str], size: tuple):
        self.instructions = self.parse_input(cube_faces)
        cube_faces = {}
        for face in range(6):
            cube_faces[face + 1] = {(row, col): 1
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
        while base_value >= 100:
            base_value -= 100
        while base_value <= 1:
            base_value += 100
        return base_value

    def print_cube(self, data: dict):

        # Helper to get a 3x3 face as list of strings
        def face_to_lines(size, face):
            return [
                " ".join(f"{face.get((i, j), ''):>2}"
                for j in range(1, size[0] +1 )) for i in range(1, size[1] + 1)
            ]

        # Get each face
        front = face_to_lines(self.CUBE_SIZE, data[1])
        bottom = face_to_lines(self.CUBE_SIZE, data[2])
        back = face_to_lines(self.CUBE_SIZE, data[3])
        top = face_to_lines(self.CUBE_SIZE, data[4])
        left = face_to_lines(self.CUBE_SIZE, data[5])
        right = face_to_lines(self.CUBE_SIZE, data[6])

        # Print net
        for row in front:
            print(" " * self.CUBE_SIZE[0]**2 + row)

        for i in range(len(left)):
            print(f"{left[i]} {bottom[i]} {right[i]}")

        for row in back:
            print(" " * self.CUBE_SIZE[0]**2 + row)

        for row in top:
            print(" " * self.CUBE_SIZE[0]**2 + row)

    def get_adjacent_face(self, twist: str, cube_map: dict, cube_faces: dict):
        """Twists the cube and rotates face data as needed."""
        # Rotate face mapping (which face is front/left/etc.)
        def rotate_face_90(cube, faces, size, clockwise=True):
            rows, cols = size
            rotated_cube = cube.copy()
            for face in faces:
                rotated = {}
                tile_dict = cube[face]
                for (i, j), val in tile_dict.items():
                    if clockwise:
                        rotated[(j, rows - i + 1)] = val
                    else:
                        rotated[(cols - j + 1, i)] = val
                rotated_cube[face] = rotated
            return rotated_cube
        new_map = cube_map.copy()

        if twist == "L":
            new_map["C"] = cube_map["L"]
            new_map["L"] = cube_map["O"]
            new_map["O"] = cube_map["R"]
            new_map["R"] = cube_map["C"]
            rotate_faces = [new_map[face] for face in "UDCLRO"]
            cube_faces = rotate_face_90(cube_faces, rotate_faces, self.CUBE_SIZE, clockwise=False)
        elif twist == "R":
            new_map["C"] = cube_map["R"]
            new_map["L"] = cube_map["C"]
            new_map["R"] = cube_map["O"]
            new_map["O"] = cube_map["L"]
            rotate_faces = [new_map[face] for face in "UDCOLR"]
            cube_faces = rotate_face_90(cube_faces, rotate_faces, self.CUBE_SIZE, clockwise=True)
        elif twist == "U":
            new_map["C"] = cube_map["U"]
            new_map["U"] = cube_map["O"]
            new_map["O"] = cube_map["D"]
            new_map["D"] = cube_map["C"]
            rotate_faces = [new_map[face] for face in "LRCOUD"]
            cube_faces = rotate_face_90(cube_faces, rotate_faces, self.CUBE_SIZE, clockwise=False)
        elif twist == "D":
            new_map["C"] = cube_map["D"]
            new_map["U"] = cube_map["C"]
            new_map["D"] = cube_map["O"]
            new_map["O"] = cube_map["U"]
            rotate_faces = [new_map[face] for face in "LRCOUD"]
            cube_faces = rotate_face_90(cube_faces, rotate_faces, self.CUBE_SIZE, clockwise=True)

        return new_map, cube_faces

    def perform_transformations(self, twists: str, visualize: bool = False):
        cube_dict = {"C": 1, "L": 5, "R": 6, "U": 4, "D": 2, "O": 3}
        current_face = cube_dict["C"]
        absorptions = {}
        cube_faces = self.cube_faces.copy()

        for idx, instruc in enumerate(self.instructions):
            face_data = cube_faces[current_face]
            updated_face = face_data.copy()
            op_type, delta = instruc[0], instruc[-1]

            if op_type == "FACE":
                for pos in face_data:
                    updated_face[pos] = self.check_value(face_data[pos] + delta)
                power = delta * self.CUBE_SIZE[0] * self.CUBE_SIZE[1]

            elif op_type == "ROW":
                for pos in face_data:
                    if pos[0] == instruc[1]:
                        updated_face[pos] = self.check_value(face_data[pos] + delta)
                power = delta * self.CUBE_SIZE[0]

            elif op_type == "COL":
                for pos in face_data:
                    if pos[1] == instruc[1]:
                        updated_face[pos] = self.check_value(face_data[pos] + delta)
                power = delta * self.CUBE_SIZE[1]

            cube_faces[current_face] = updated_face
            absorptions[current_face] = absorptions.get(current_face, 0) + power
            if visualize:
                print(instruc)
                self.print_cube(cube_faces)

            # Apply twist if available
            if idx < len(twists):
                twist_dir = twists[idx]
                cube_dict, cube_faces = self.get_adjacent_face(twist_dir, cube_dict, cube_faces)
                if visualize:
                    print(f"{twist_dir}: {current_face} -> {cube_dict['C']}")
                    self.print_cube(cube_faces)
                    print("_____________________________________")
                current_face = cube_dict["C"]
        # self.print_cube(cube_faces)
        return absorptions, cube_faces

    def calculate_dominant_sums(self, cube_face):
        # self.print_cube(cube_face)
        dominant_list = []
        for face, tile_dict in cube_face.items():
            row_vals = {num + 1: 0 for num in range(self.CUBE_SIZE[0])}
            col_vals = {num + 1: 0 for num in range(self.CUBE_SIZE[1])}
            for pos, tile in tile_dict.items():
                row_vals[pos[0]] += tile
                col_vals[pos[1]] += tile
            # print(face, max(row_vals.values()), max(col_vals.values()))
            dominant_list.append(max(max(row_vals.values()), max(col_vals.values())))
        return np.prod(dominant_list)

cubes = MindCube(instructions, cube_size)

absorption, final_cube = cubes.perform_transformations(directions)
print("Part 1:", np.prod(sorted(absorption.values(), reverse=True)[:2]))

final_cube1 = {
    1: {(1, 1): 7, (1, 2): 39, (1, 3): 39, (2, 1): 7, (2, 2): 39, (2, 3): 39, (3, 1): 7, (3, 2): 39, (3, 3): 39},
    2: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 1, (2, 3): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1},
    3: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 1, (2, 3): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1},
    4: {(1, 1): 1, (1, 2): 1, (1, 3): 58, (2, 1): 1, (2, 2): 1, (2, 3): 58, (3, 1): 1, (3, 2): 1, (3, 3): 58},
    5: {(1, 1): 53, (1, 2): 72, (1, 3): 1, (2, 1): 53, (2, 2): 72, (2, 3): 1, (3, 1): 53, (3, 2): 72, (3, 3): 1},
    6: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 1, (2, 3): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1},

}

dominant_sum = cubes.calculate_dominant_sums(final_cube)
print("Part 2:", dominant_sum) # 369594451623936000000

print(f"Execution Time = {time.time() - start_time:.5f}s")

#          7  39 39
#          7  39 39
#          7  39 39
# 53 72 1  1  1  1  1  1  1
# 53 72 1  1  1  1  1  1  1
# 53 72 1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  58
#          1  1  58
#          1  1  58

# When each value on the grid of each face is written out:

#          1  1  1
#          1  1  1
#          1  1  1
# 1  1  1  1  1  1  1  1  1
# 1  1  1  1  1  1  1  1  1
# 1  1  1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1


# The first instruction, ‘FACE - VALUE 38’, is performed on face 1.
#          39 39 39
#          39 39 39
#          39 39 39
# 1  1  1  1  1  1  1  1  1
# 1  1  1  1  1  1  1  1  1
# 1  1  1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1


# Then, the twist “L” is performed, and the ‘current face’ changes to face 5.
# The second instruction, ‘ROW 2 - VALUE 71’, is performed on face 5.

#          39 39 39
#          39 39 39
#          39 39 39
# 1  72 1  1  1  1  1  1  1
# 1  72 1  1  1  1  1  1  1
# 1  72 1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  1


# The twist “U” is performed, and the ‘current face’ changes to face 4.

# The third instruction, ‘ROW 1 - VALUE 57’, is performed on face 4.

#          39 39 39
#          39 39 39
#          39 39 39
# 1  72 1  1  1  1  1  1  1
# 1  72 1  1  1  1  1  1  1
# 1  72 1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  58
#          1  1  58
#          1  1  58


# The twist “R” is performed, and the ‘current face’ changes to face 1.

# The fourth instruction, ‘ROW 3 - VALUE 68’, is performed on face 1.

#          7  39 39
#          7  39 39
#          7  39 39
# 1  72 1  1  1  1  1  1  1
# 1  72 1  1  1  1  1  1  1
# 1  72 1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  58
#          1  1  58
#          1  1  58


# The twist “D” is performed, and the ‘current face’ changes to face 5.

# The final instruction, ‘COL 1 - VALUE 52’, is performed on face 5.

#          7  39 39
#          7  39 39
#          7  39 39
# 53 72 1  1  1  1  1  1  1
# 53 72 1  1  1  1  1  1  1
# 53 72 1  1  1  1  1  1  1
#          1  1  1
#          1  1  1
#          1  1  1
#          1  1  58
#          1  1  58
#          1  1  58

# The product of the dominant sums on each face is therefore 118727856.