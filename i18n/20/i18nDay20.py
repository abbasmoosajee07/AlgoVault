"""i18n Puzzles - Puzzle 20
Solution Started: Jun 19, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/20
Solution by: Abbas Moosajee
Brief: [The future of Unicode]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import unicodedata
start_time = time.time()

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')

class UnicodeEncryptor:
    def __init__(self):
        self.test_message = self.__get_test("test_input.txt")
        self.decoded_test = "ꪪꪪꪪ This is a secret message. ꪪꪪꪪ Good luck decoding me! ꪪꪪꪪ"

    def __get_test(self, file_name):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        with open(test_file) as file:
            input_data = file.read().strip().split('\n')
        return input_data

    def decode_message(self, encrypted):
        print('\n'.join(self.test_message))
        print(unicodedata.unidata_version)

        # print('\n'.join(encrypted))

decoded = UnicodeEncryptor().decode_message(input_data)
print(f"Execution Time = {time.time() - start_time:.5f}s")
