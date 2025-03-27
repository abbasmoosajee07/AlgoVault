"""i18n Puzzles - Puzzle 13
Solution Started: Mar 25, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/13/
Solution by: Abbas Moosajee
Brief: [Gulliver's puzzle dictionary]
"""

#!/usr/bin/env python3

import os, unicodedata

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n\n')

dictionary = input_data[0].split('\n')
crossword = input_data[1].split('\n')

# List of possible encodings
possible_formats = ["utf-8", "utf-16-be", "iso-8859-1", "utf-16-le"]

def decode_word(encoded_string: str) -> str:

    def hex_to_bytes(hex_string: str) -> bytes:
        return bytes(
            int(hex_string[i:i + 2], 16)
            for i in range(0, len(hex_string), 2)
        )

    def is_latin_word(word: str) -> bool:
        return all(
            unicodedata.category(char) in ["Lu", "Ll"]
            for char in word
        )

    decoded_list = []
    # Example list of hex-encoded strings
    # dictionary should be defined before use
    bytes_object = hex_to_bytes(encoded_string)

    # Remove BOM if present
    if bytes_object.startswith(b'\xef\xbb\xbf'):
        bytes_object = bytes_object[3:]
    elif bytes_object.startswith(b'\xff\xfe'):
        bytes_object = bytes_object[2:]
    elif bytes_object.startswith(b'\xfe\xff'):
        bytes_object = bytes_object[2:]

    # Decode and print result
    results: set[str] = set()
    for encoding in possible_formats:
        try:
            decoding = bytes_object.decode(encoding)
            if is_latin_word(decoding):
                results.add(decoding)
        except UnicodeDecodeError:
            pass
    if len(results) != 1:
        print(f"{len(results)} possibilities for {bytes_object}: {results}")
    decoded_word =  results.pop() if results else ""
    # print(f"{encoded_string} -> {decoded_word}")
    return decoded_word

decoded_dictionary = [decode_word(string) for string in dictionary]


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
corrected_list_lower = [word.lower() for word in decoded_dictionary]  # Precompute lowercase words

for empty_word in crossword:
    stripped_word = empty_word.strip()
    for word_no, word_lower in enumerate(corrected_list_lower, start=1):
        if find_match_words(stripped_word, word_lower):
            line_sum += word_no
            break  # Stop after first match per line

print("Word Line Numbers:", line_sum)