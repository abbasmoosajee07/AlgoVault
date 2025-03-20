"""i18n Puzzles - Puzzle 11
Solution Started: Mar 17, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/11/
Solution by: Abbas Moosajee
Brief: [Homer's Cipher]
"""

#!/usr/bin/env python3

import os, re


# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n')

# Dictionary for Greek-to-Latin transliteration of "Odysseus"
odyssey_list = [
    "Οδυσσευς - Odysseus", "Οδυσσεως - Odysseos", "Οδυσσει - Odyssei",
    "Οδυσσεα - Odyssea", "Οδυσσευ - Odysseu"
]
odyssey_dict = {greek: latin for line in odyssey_list for greek, latin in [line.split(" - ", 1)]}

# Greek alphabet mappings
CAPITAL_GREEK = list("ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
SIMPLE_GREEK = list("αβγδεζηθικλμνξοπρστυφχψω")
SIGMA, FINAL_SIGMA = "σ", "ς"

# Regex pattern for extracting words
WORDS_PATTERN = re.compile(r"\w+")

def shift_greek(text: str, shift: int) -> str:
    """Shifts Greek letters by a given amount within the alphabet."""
    def shift_letter(char: str) -> str:
        if char == FINAL_SIGMA:
            char = SIGMA

        for alphabet in (CAPITAL_GREEK, SIMPLE_GREEK):
            if char in alphabet:
                return alphabet[(alphabet.index(char) + shift) % len(alphabet)]

        return char  # Keep non-Greek characters unchanged

    return "".join(shift_letter(char) for char in text)

def find_shift(text: str, targets: list[str]) -> int | None:
    """Finds the shift degree that makes a target Greek word appear in the text."""
    for shift in range(24):
        shifted_text = shift_greek(text, shift)
        if any(target in WORDS_PATTERN.findall(shifted_text) for target in targets):
            return shift
    return None

"""Processes each line to determine necessary alphabet shifts."""
targets = [shift_greek(word, 0) for word in odyssey_dict.keys()]
total_shifts = sum(find_shift(line, targets) or 0 for line in input_data)
print("Total Alphabet Shifts:", total_shifts)

