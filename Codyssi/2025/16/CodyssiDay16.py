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

    def rotate_face(self, cube, face, clockwise=True):
        rows, cols = self.CUBE_SIZE
        rotated_cube = cube.copy()
        rotated = {}
        tile_dict = cube[face]
        for (i, j), val in tile_dict.items():
            if clockwise:
                rotated[(j, rows - i + 1)] = val
            else:
                rotated[(cols - j + 1, i)] = val
        rotated_cube[face] = rotated
        return rotated_cube

    def twist_U(self, cube_faces, new_map) -> None:
        cube_faces = self.rotate_face(cube_faces, new_map["L"], False)  # Rotate the top face counterclockwise
        cube_faces = self.rotate_face(cube_faces, new_map["R"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["O"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["O"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["D"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["D"], True)  # Rotate the bottom face clockwise
        return cube_faces

    def twist_D(self, cube_faces, new_map) -> None:
        cube_faces = self.rotate_face(cube_faces, new_map["R"], False)  # Rotate the top face counterclockwise
        cube_faces = self.rotate_face(cube_faces, new_map["L"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["U"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["U"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["O"], True)  # Rotate the bottom face clockwise
        cube_faces = self.rotate_face(cube_faces, new_map["O"], True)  # Rotate the bottom face clockwise
        return cube_faces

    def twist_L(self, cube_faces, new_map) -> None:
        cube_faces = self.rotate_face(cube_faces, new_map["U"], False)  # Rotate the up face counterclockwise
        cube_faces = self.rotate_face(cube_faces, new_map["D"], True)   # Rotate the down face clockwise
        return cube_faces

    def twist_R(self, cube_faces, new_map) -> None:
        cube_faces = self.rotate_face(cube_faces, new_map["U"], False)  # Rotate the up face counterclockwise
        cube_faces = self.rotate_face(cube_faces, new_map["D"], True)   # Rotate the down face clockwise
        return cube_faces

    def print_cube(self, data: dict):
        # Helper to get a 3x3 face as list of strings
        def face_to_lines(size, face):
            return [
                " ".join(f"{face.get((i, j), ''):>2}"
                for j in range(1, size[0] + 1)) for i in range(1, size[1] + 1)
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

        new_map = cube_map.copy()

        if twist == "L":
            cube_faces = self.twist_L(cube_faces, cube_map)
            new_map["C"] = cube_map["L"]
            new_map["L"] = cube_map["O"]
            new_map["O"] = cube_map["R"]
            new_map["R"] = cube_map["C"]

        elif twist == "R":
            cube_faces = self.twist_R(cube_faces, cube_map)
            new_map["C"] = cube_map["R"]
            new_map["L"] = cube_map["C"]
            new_map["R"] = cube_map["O"]
            new_map["O"] = cube_map["L"]

        elif twist == "U":
            cube_faces = self.twist_U(cube_faces, cube_map)
            new_map["C"] = cube_map["U"]
            new_map["U"] = cube_map["O"]
            new_map["O"] = cube_map["D"]
            new_map["D"] = cube_map["C"]

        elif twist == "D":
            cube_faces = self.twist_D(cube_faces, cube_map)
            new_map["C"] = cube_map["D"]
            new_map["U"] = cube_map["C"]
            new_map["D"] = cube_map["O"]
            new_map["O"] = cube_map["U"]

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
                    # self.print_cube(cube_faces)
                    print("_____________________________________")
                current_face = cube_dict["C"]
        # self.print_cube(cube_faces)
        return absorptions, cube_faces

    def calculate_dominant_sums(self, cube_face):
        dominant_list = []
        for face, tile_dict in cube_face.items():
            row_vals = {num + 1: 0 for num in range(self.CUBE_SIZE[0])}
            col_vals = {num + 1: 0 for num in range(self.CUBE_SIZE[1])}
            for pos, tile in tile_dict.items():
                row_vals[pos[0]] += tile
                col_vals[pos[1]] += tile
            dominant_list.append(max(max(row_vals.values()), max(col_vals.values())))
        return np.prod(dominant_list)


class MindCube:
    def __init__(self, cube_faces: list[str], size: tuple):
        self.instructions = self.parse_input(cube_faces)
        self.twists = []
        self.CUBE_SIZE = size
        self.faces = {coords: np.full((size[0], size[1]), 1, dtype=object) 
                        for coords in ['x','y','z','-x','-y','-z']}
        self.orientations = {
            'L': {'x':['-y',0],'-y':['-x',0],'-x':['y',0],'y':['x',0],'z':['z',1],'-z':['-z',3]},
            'R': {'x':['y',0],'y':['-x',0],'-x':['-y',0],'-y':['x',0],'z':['z',3],'-z':['-z',1]},
            'D': {'y':['z',0],'z':['-y',2],'-y':['-z',0],'-z':['y',2],'x':['x',3],'-x':['-x',1]},
            'U': {'y':['-z',2],'-z':['-y',0],'-y':['z',2],'z':['y',0],'x':['x',1],'-x':['-x',3]}
        }

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

    def rotate(self, twist):
        def self_rotate(face, num):
            for _ in range(num):
                face = np.rot90(face)
            return face

        rotate_dict = self.orientations[twist]
        self.faces = {
            key: self_rotate(self.faces[output], num) 
            for key, (output, num) in rotate_dict.items()
        }

    def perform_transformations(self, twists: str, visualize: bool = False):
        self.twists = list(twists)
        self.twists.append('')  # Match length with instructions

        for (idx, instruc) in enumerate(self.instructions):
            twist = self.twists[idx]
            if instruc[0] == "FACE":
                self.faces['-y'] = (self.faces['-y'] + instruc[1] - 1) % 100 + 1
            elif instruc[0] == "ROW":
                self.faces['-y'][instruc[1] - 1, :] = (self.faces['-y'][instruc[1] - 1, :] + instruc[2] - 1) % 100 + 1
            elif instruc[0] == "COL":
                self.faces['-y'][:, instruc[1] - 1] = (self.faces['-y'][:, instruc[1] - 1] + instruc[2] - 1) % 100 + 1

            if twist != '':
                self.rotate(twist)

    def calculate_dominant_sums(self):
        def dominant_sum(face):
            rowmax = max(sum(row) for row in face)
            colmax = max(sum(row) for row in np.rot90(face))
            return max(rowmax, colmax)

        dominant_sums = [dominant_sum(face) for face in self.faces.values()]
        result = 1
        for num in dominant_sums:
            result *= num
        return result

class MindCube:
    def __init__(self, cube_faces: list[str], size: tuple):
        self.instructions = self.parse_input(cube_faces)
        self.twists = []
        self.CUBE_SIZE = size
        self.faces = {
            face: {
                (i, j): 1
                for i in range(1, size[0] + 1)
                for j in range(1, size[1] + 1)
            }
            for face in ['x', 'y', 'z', '-x', '-y', '-z']
        }
        self.orientations = {
            'L': {'x': ['-y', 0], '-y': ['-x', 0], '-x': ['y', 0], 'y': ['x', 0], 'z': ['z', 1], '-z': ['-z', 3]},
            'R': {'x': ['y', 0], 'y': ['-x', 0], '-x': ['-y', 0], '-y': ['x', 0], 'z': ['z', 3], '-z': ['-z', 1]},
            'D': {'y': ['z', 0], 'z': ['-y', 2], '-y': ['-z', 0], '-z': ['y', 2], 'x': ['x', 3], '-x': ['-x', 1]},
            'U': {'y': ['-z', 2], '-z': ['-y', 0], '-y': ['z', 2], 'z': ['y', 0], 'x': ['x', 1], '-x': ['-x', 3]}
        }

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

    def rotate_dict_face(self, face_data, times):
        rows, cols = self.CUBE_SIZE
        rotated = face_data.copy()
        for _ in range(times):
            new_data = {}
            for (i, j), val in rotated.items():
                new_data[(j, rows - i + 1)] = val
            rotated = new_data
        return rotated

    def rotate(self, twist):
        rotate_dict = self.orientations[twist]
        self.faces = {
            key: self.rotate_dict_face(self.faces[output], times)
            for key, (output, times) in rotate_dict.items()
        }

    def check_value(self, val):
        while val > 100:
            val -= 100
        while val < 1:
            val += 100
        return val

    def perform_transformations(self, twists: str, visualize: bool = False):
        self.twists = list(twists)
        self.twists.append('')  # Match length with instructions

        for idx, instruc in enumerate(self.instructions):
            twist = self.twists[idx]
            face = self.faces['-y']
            updated = face.copy()
            if instruc[0] == "FACE":
                for pos in face:
                    updated[pos] = self.check_value(face[pos] + instruc[1])
            elif instruc[0] == "ROW":
                for (i, j) in face:
                    if i == instruc[1]:
                        updated[(i, j)] = self.check_value(face[(i, j)] + instruc[2])
            elif instruc[0] == "COL":
                for (i, j) in face:
                    if j == instruc[1]:
                        updated[(i, j)] = self.check_value(face[(i, j)] + instruc[2])

            self.faces['-y'] = updated
            if twist:
                self.rotate(twist)

    def calculate_dominant_sums(self):
        def dominant_sum(face_dict):
            row_totals = {i: 0 for i in range(1, self.CUBE_SIZE[0] + 1)}
            col_totals = {j: 0 for j in range(1, self.CUBE_SIZE[1] + 1)}
            for (i, j), val in face_dict.items():
                row_totals[i] += val
                col_totals[j] += val
            return max(max(row_totals.values()), max(col_totals.values()))

        product = 1
        for face in self.faces.values():
            product *= dominant_sum(face)
        return product

cubes = MindCube(instructions, cube_size)


absorption = cubes.perform_transformations(directions)
# print("Part 1:", np.prod(sorted(absorption.values(), reverse=True)[:2]))

final_cube1 = {
    1: {(1, 1): 7, (1, 2): 39, (1, 3): 39, (2, 1): 7, (2, 2): 39, (2, 3): 39, (3, 1): 7, (3, 2): 39, (3, 3): 39},
    2: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 1, (2, 3): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1},
    3: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 1, (2, 3): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1},
    4: {(1, 1): 1, (1, 2): 1, (1, 3): 58, (2, 1): 1, (2, 2): 1, (2, 3): 58, (3, 1): 1, (3, 2): 1, (3, 3): 58},
    5: {(1, 1): 53, (1, 2): 72, (1, 3): 1, (2, 1): 53, (2, 2): 72, (2, 3): 1, (3, 1): 53, (3, 2): 72, (3, 3): 1},
    6: {(1, 1): 1, (1, 2): 1, (1, 3): 1, (2, 1): 1, (2, 2): 1, (2, 3): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1},

}

dominant_sum = cubes.calculate_dominant_sums()
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