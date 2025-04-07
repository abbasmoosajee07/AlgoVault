"""Codyssi Puzzles - Problem 2
Solution Started: Apr 6, 2025
Puzzle Link: https://www.codyssi.com/view_problem_2?
Solution by: Abbas Moosajee
Brief: [Sensors and Circuits!]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data1 = "TRUE\nFALSE\nTRUE\nFALSE\nFALSE\nFALSE\nTRUE\nTRUE\n".splitlines()
true_ids = [id_val for id_val, output in enumerate(input_data, start=1) if output == "TRUE"]
print("Part 1:", sum(true_ids))

sensor_pairs = [tuple(input_data[i:i+2]) for i in range(0, len(input_data), 2)]

gates_count = 0
for idx, (out_1, out_2) in enumerate(sensor_pairs, start=1):
    if idx % 2 == 0:  # OR gate
        if "TRUE" in (out_1, out_2):
            gates_count += 1
    else:  # AND gate
        if out_1 == "TRUE" and out_2 == "TRUE":
            gates_count += 1

print("Part 2:", gates_count)

def count_true_outputs(sensor_outputs):
    total_true = sensor_outputs.count("TRUE")  # Start with sensor TRUEs
    current_layer = sensor_outputs.copy()
    layer_index = 0

    while len(current_layer) > 1:
        next_layer = []
        for i in range(0, len(current_layer) - 1, 2):
            out1, out2 = current_layer[i], current_layer[i + 1]
            is_even_gate = (i // 2 + 1) % 2 == 0  # 1-based index for gates

            if is_even_gate:  # OR gate
                result = "TRUE" if "TRUE" in (out1, out2) else "FALSE"
            else:  # AND gate
                result = "TRUE" if out1 == "TRUE" and out2 == "TRUE" else "FALSE"

            next_layer.append(result)
            if result == "TRUE":
                total_true += 1

        # If there's an odd one out, carry it forward
        if len(current_layer) % 2 == 1:
            next_layer.append(current_layer[-1])

        current_layer = next_layer
        layer_index += 1

    return total_true


print("Part 3:",count_true_outputs(input_data))