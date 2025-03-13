"""i18n Puzzles - Puzzle 6
Solution Started: Mar 12, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/6/
Solution by: Abbas Moosajee
Brief: [Mojibake puzzle dictionary]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n\n')

test_input = ['geléet\nträffs\nreligiÃ«n\ntancées\nkÃ¼rst\nroekoeÃ«n\nskälen\nböige\nfÃ¤gnar\ndardÃ©es\namènent\norquestrÃ¡\nimputarão\nmolières\npugilarÃ\x83Â£o\nazeitámos\ndagcrème\nzÃ¶ger\nondulât\nblÃ¶kt', '   ...d...\n    ..e.....\n     .l...\n  ....f.\n......t..']
# input_data = test_input

list_of_words = input_data[0].split('\n')
crossword = input_data[1].split('\n')

def fix_encoding(text: str) -> str:
    """Fixes text that was originally UTF-8 but misinterpreted as ISO-8859-1 before being stored as UTF-8."""
    try:
        return text.encode('iso-8859-1').decode('utf-8')
    except UnicodeEncodeError:
        return text  # If already correct, return as is

# Precompute fixed words efficiently
corrected_list = [
    fix_encoding(fix_encoding(word)) if word_no % 15 == 0 else
    fix_encoding(word) if word_no % 3 == 0 or word_no % 5 == 0 else 
    word
    for word_no, word in enumerate(list_of_words, start=1)
]

def find_match_words(word_space: str, test_word: str) -> bool:
    """Checks if a test word matches a word space with letter constraints.
       Matching is case-insensitive but accent-sensitive.
    """
    if len(word_space) != len(test_word):
        return False

    constraints = {pos: letter for pos, letter in enumerate(word_space) if letter != '.'}
    
    # If no constraints, return False immediately
    if not constraints:
        return False  

    # Convert test_word to lowercase only once
    test_word_lower = test_word.lower()

    # Check constraints efficiently
    return all(test_word_lower[pos] == letter for pos, letter in constraints.items())

# Process words once and store matching indices
line_sum = 0
corrected_list_lower = [word.lower() for word in corrected_list]  # Precompute lowercase words

for empty_word in crossword:
    stripped_word = empty_word.strip()
    for word_no, word_lower in enumerate(corrected_list_lower, start=1):
        if find_match_words(stripped_word, word_lower):
            line_sum += word_no
            break  # Stop after first match per line

print("Word Line Numbers:", line_sum)
