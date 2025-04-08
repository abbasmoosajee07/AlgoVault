"""Codyssi Puzzles - Problem 4
    Solution Started: Apr 8, 2025
    Puzzle Link: https://www.codyssi.com/view_problem_8?
    Solution by: Abbas Moosajee
    Brief: [Aeolian Transmissions]
    """

#!/usr/bin/env python3

import os, re, copy, string

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n')

LETTER_DICT = {letter: idx for idx, letter in enumerate(string.ascii_uppercase, start=1)}
NUMBER_DICT = {num_str: idx for idx, num_str in enumerate("0123456789")}
COMBINED_DICT = {**LETTER_DICT, **NUMBER_DICT}

memory_reqd = [LETTER_DICT[letter] for letter in ''.join(input_data)]
print("Part 1:", sum(memory_reqd))

def compress_file(file_data: str) -> int:
    file_len = len(file_data)
    save_chars = file_len // 10
    comp_data = file_len - (save_chars * 2)
    new_file = f"{file_data[:save_chars]}{comp_data}{file_data[-save_chars:]}"
    comp_file_size = [COMBINED_DICT[char_str] for char_str in new_file]
    # print(f"{file_data} -> {new_file}, Comp_size: {sum(comp_file_size)}")
    return sum(comp_file_size)

memory_comp = [compress_file(file_data) for file_data in input_data]
print("Part 2:", sum(memory_comp))

def lossless_compression(file_data: str) -> int:
    file_len = len(file_data)
    new_file = ""
    count = 1
    for idx, char in enumerate(file_data):
        if (idx + 1) < file_len and char == file_data[idx + 1]:
            count += 1
        else:
            new_file += f"{count}{char}"
            count = 1
    comp_file_size = [COMBINED_DICT[char_str] for char_str in new_file]
    # print(f"{file_data} -> {new_file}, Comp_size: {sum(comp_file_size)}")
    return sum(comp_file_size)

memory_lossless = [lossless_compression(file_data) for file_data in input_data]
print("Part 2:", sum(memory_lossless))
