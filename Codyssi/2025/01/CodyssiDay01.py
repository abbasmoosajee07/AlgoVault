"""Codyssi Puzzles - Problem 1
Solution Started: Apr 6, 2025
Puzzle Link: https://www.codyssi.com/view_problem_5?
Solution by: Abbas Moosajee
Brief: [Compass Calibration]
"""

#!/usr/bin/env python3

import os, re, copy

# Load the input data from the specified file path
D01_file = "Day01_input.txt"
D01_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D01_file)

# Read and sort input data into a grid
with open(D01_file_path) as file:
    input_data = file.read().strip().split('\n')
    measurements = list(map(int, input_data[:-1]))
    offsets = input_data[-1]

def calibrate_compass(measurements: list[int], offsets: list[str]) -> int:
    values = measurements[1:]
    corrected_value = measurements[0]
    for sign, value in zip(offsets, values):
        # print(sign, value, corrected_value)
        if sign == '+':
            corrected_value += value
        elif sign == '-':
            corrected_value -= value
    return corrected_value

calibration_p1 = calibrate_compass(measurements, offsets)
print("Part 1:", calibration_p1)

calibration_p2 = calibrate_compass(measurements, offsets[::-1])
print("Part 2:", calibration_p2)

paired_measurements = [int(f"{measurements[i]}{measurements[i+1]}") for i in range(0, len(measurements) - 1, 2)]
calibration_p3 = calibrate_compass(paired_measurements, offsets[::-1])
print("Part 3:", calibration_p3)