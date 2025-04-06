"""piDay Puzzles - 2024
Solution Started: Apr 5, 2025
Puzzle Link: https://ivanr3d.com/projects/pi/2024.html
Solution by: Abbas Moosajee
Brief: [Ceaser Cipher with Pi key]
"""

#!/usr/bin/env python3

import os, re, copy, string, time

start_time = time.time()

# Load the input data from the specified file path
D2024_file = "Day2024_input.txt"
D2024_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2024_file)

# Read and sort input data into a grid
with open(D2024_file_path) as file:
    input_data = file.read().strip().split('\n')[0]

# Configuration
pi_value = "3.141592653589793238462643"
pi_list = [int(num) for num in pi_value if num != '.']
letter_list = list(string.ascii_lowercase)
num_dicts = {
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'
}

# Pi-based letter shifting decode
output = ""
pi_index = 0

for char in input_data:
    if char.isalpha():
        is_upper = char.isupper()
        base_char = char.lower()
        char_index = letter_list.index(base_char)

        # Get next digit from pi and apply leftward shift
        shift = pi_list[pi_index]
        shifted_index = (char_index - shift) % 26
        shifted_char = letter_list[shifted_index]

        output += shifted_char.upper() if is_upper else shifted_char
    else:
        output += char

    # Cycle through the pi digits
    pi_index = (pi_index + 1) % 16

# Clean and extract message for password computation
message_clean = ''.join(c for c in output.lower() if c.isalpha())

# Build the cipher password based on word frequencies
cipher_password = 1
digits = []

for number, word in num_dicts.items():
    occurrences = len(list(re.finditer(word, message_clean)))
    digits.extend([number] * occurrences)
    for _ in range(occurrences):
        cipher_password *= number

# Final output
print("Encoded:", input_data)
print("Decoded:", output)
print("Cipher Password:", cipher_password)

print(f"Execution Time = {time.time() - start_time:.5f}s")
