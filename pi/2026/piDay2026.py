"""piDay Puzzles - 2026
Solution Started: Mar 14, 2026
Puzzle Link: https://ivanr3d.com/projects/pi/2026.html
Solution by: Abbas Moosajee
Brief: [π-Ghost Signal]
"""

#!/usr/bin/env python3

from collections import Counter, defaultdict
from heapq import heappush, heappop
import os, re, time, textwrap
from mpmath import mp

print("pi Day 2026:  π-Ghost Signal")

start_time = time.time()

input_file = "Day2026_input.txt"
input_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_file)


with open(input_file_path) as file:
    input_data = file.read().strip().split('\n\n')

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

def split_text(signal: str) -> list[str]:
    split_words = re.split(r' {4,}', signal)
    return split_words

def decode_morse_code(morse_input):
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
    return "\n".join(decoded_phrase)

# --------------Part 1--------------
decoded_phrase = decode_morse_code(input_data)
print("Part 1 - Decoded Phrase:", decoded_phrase)

# --------------Part 2--------------
def calc_digit_cost(digit):
    # 3 × (number of dashes) + 1 × (number of dots) + digit
    morse_digit = MORSE_CODE_DICT[digit]
    morse_counter = Counter(morse_digit)
    return 3 * morse_counter["-"] + 1 * morse_counter["."] + int(digit)

def print_pi_grid(pi_grid):
    size = int(len(pi_grid) ** 0.5)
    for i in range(size):
        print(' '.join(f"{pi_grid[(i,j)]:2}" for j in range(size)))

def build_pi_grid(grid_size):
    grid_dict = defaultdict(tuple)
    mp.dps = grid_size ** 2
    pi_digits = f"{mp.pi}".replace(".", "")
    grid_rows = textwrap.wrap(pi_digits, grid_size)
    for row_no, row_data in enumerate(grid_rows):
        for col_no, digit in enumerate(row_data):
            digit_cost = calc_digit_cost(digit)
            grid_dict[(row_no, col_no)] = digit_cost
    return grid_dict

MOVE_DIR = {(1, 0): "v", (-1, 0): "^", (0, 1): ">", (0, -1): "<"}

def min_path(grid):
    start, goal = min(grid), max(grid)

    pq = []
    heappush(pq, (grid[start], start, [start]))

    visited = set()
    min_cost, min_path = float("inf"), []

    while pq:
        cost, pos, path = heappop(pq)

        if pos in visited:
            continue
        visited.add(pos)

        if pos == goal:
            if cost <= min_cost:
                min_cost = cost
                min_path = path
            continue

        for dr, dc in MOVE_DIR:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if new_pos in grid:
                new_cost = cost + grid[new_pos]
                heappush(pq, (new_cost, new_pos, path + [new_pos]))
    return len(min_path) * min_cost

pi_grid = build_pi_grid(100)
path_password = min_path(pi_grid)
print("Part 2 - Grid Passcode:", path_password)

print(f"Execution Time = {time.time() - start_time:.5f}s")
