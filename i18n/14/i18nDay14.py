"""i18n Puzzles - Puzzle 14
Solution Started: Mar 27, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/14/
Solution by: Abbas Moosajee
Brief: [Metrification in Japan]
"""

#!/usr/bin/env python3

import os, fractions
# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path, encoding = "utf-8") as file:
    input_data = file.read().strip().split('\n')

def read_japanese_number(japanese_script: str) -> int:
    SMALL_NUMBERS = {"一":1, "二":2, "三":3, "四":4, "五":5, "六":6, "七":7, "八":8, "九":9}
    POWERS_TEN = {"十":10, "百":100, "千":1000}
    LARGE_UNITS = {"万":10000, "億":100000000}

    total = 0
    current_unit = 0  # Holds values within each large unit (万, 億)
    last_number = 0   # Tracks the last small number seen

    for char in japanese_script:
        if char in SMALL_NUMBERS:
            last_number = SMALL_NUMBERS[char]  # Store number to be multiplied later
        elif char in POWERS_TEN:
            multiplier = POWERS_TEN[char]
            if last_number == 0:
                last_number = 1  # Handle implicit "one" (e.g., 百 = 100)
            current_unit += last_number * multiplier
            last_number = 0  # Reset the last number since it's used
        elif char in LARGE_UNITS:
            multiplier = LARGE_UNITS[char]
            total += (current_unit + last_number) * multiplier
            current_unit = 0  # Reset the current unit after applying the large unit
            last_number = 0  # Reset last number after large unit multiplier

    total += current_unit + last_number  # Add any remaining numbers
    # print(japanese_script, "->", total)
    return total

def measure_length(full_equation: str) -> int:
    UNITS = {
        "間": fractions.Fraction(6), "丈": fractions.Fraction(10), "町": fractions.Fraction(360), "里": fractions.Fraction(12960),
        "毛": fractions.Fraction(1, 10000), "厘": fractions.Fraction(1, 1000), "分": fractions.Fraction(1, 100), 
        "寸": fractions.Fraction(1, 10), "尺": fractions.Fraction(1)
    }

    shaku_to_m = fractions.Fraction(10, 33)  # Convert 'shaku' to meters

    # Flexible split to handle spaces and different input formats
    width_part, height_part = full_equation.split(" × ")

    # Extract numbers and units
    width_num = read_japanese_number(width_part[:-1])
    height_num = read_japanese_number(height_part[:-1])
    width_unit = UNITS[width_part[-1]]
    height_unit = UNITS[height_part[-1]]

    # Compute area in square meters
    total_area = (width_num * width_unit * shaku_to_m) * (height_num * height_unit * shaku_to_m)

    # print(f"{width_part} × {height_part} = {width_num} {width_part[-1]} * {height_num} {height_part[-1]} = {int(total_area)} m²")
    return int(total_area)

total_area = [measure_length(equation) for equation in input_data]
print("Total Area:", sum(total_area))

