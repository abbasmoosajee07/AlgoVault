"""piDay Puzzles - 2026
Solution Started: Mar 14, 2026
Puzzle Link: https://ivanr3d.com/projects/pi/2026.html
Solution by: Abbas Moosajee
Brief: [ π-Ghost Signal]
"""

#!/usr/bin/env python3

import os, re, copy, time, string
import pandas as pd

start_time = time.time()

input_file = "Day2026_input.txt"
input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file)


with open(input_file_path) as file:
    input_data = file.read().strip().split('\n\n')

input_data1 = ["....  .  -.--  ,     -..  ..  -..      -.--  ---  ..-     -.-  -.  ---  .--      -  ....  .-  -     π  --.  ....  ---  ...  -      .-..  ---  ...-  .  ...     .--.  ..  .  ...  ?"]
def split_text(signal: str) -> list[str]:
    split_words = re.split(r' {4,}', signal)
    return split_words

def decode_morse_code(morse_input):

    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '0': '-----',
    }

    MORSE_DICT_REV = {value: key for key, value in MORSE_CODE_DICT.items()}
    decoded_phrase = []

    for morse_row in morse_input:
        words_list = split_text(morse_row)
        decoded_row = ""
        for word in words_list:
            decoded_word = ""
            for char in word.split():
                decoded_char = MORSE_DICT_REV.get(char, char + " ")
                decoded_word += decoded_char
            decoded_row += decoded_word + " "
        decoded_phrase.append((decoded_row))
    print("\n".join(decoded_phrase))


decode_morse_code(input_data)