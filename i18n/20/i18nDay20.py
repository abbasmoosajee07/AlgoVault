"""i18n Puzzles - Puzzle 20
Solution Started: Jun 19, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/20
Solution by: Abbas Moosajee
Brief: [The future of Unicode]
"""

#!/usr/bin/env python3

import os, re, copy, time , more_itertools, base64
import numpy as np
import pandas as pd
from struct import unpack
start_time = time.time()

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')

class UnicodeEncryptor:
    string_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.test_message = self.__get_test("test_input.txt")
        self.decoded_test = "ꪪꪪꪪ This is a secret message. ꪪꪪꪪ Good luck decoding me! ꪪꪪꪪ"

    def __get_test(self, file_name):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        with open(test_file) as file:
            input_data = file.read().strip().split('\n')
        return input_data

    def __get_utf_text(self, encoded_message):
        bytes_data = base64.b64decode(encoded_message)
        if bytes_data.startswith(b'\xff\xfe'):
            encoding_type =  "utf-16-le"
        elif bytes_data.startswith(b'\xfe\xff'):
            encoding_type =  "utf-16-be"
        elif bytes_data.startswith(b'\xef\xbb\xbf'):
            encoding_type =  "utf-8-sig"  # UTF-8 BOM is 3 bytes
        else:
            encoding_type =  "utf-8"  # Default fallback
        utf_text = bytes_data.decode(encoding_type)

        if self.debug:
            print(" Init Message:", encoded_message)
            print("Decoded bytes:", bytes_data)
            print("Encoding Type:", encoding_type)
            print(" Decoded text:", utf_text)
        return utf_text

    def decode_message(self, encrypted):
        encrypted = self.test_message
        self.debug = True
        joined_message = ''.join(encrypted)
        utf_text = self.__get_utf_text(joined_message)

        return

decoded = UnicodeEncryptor().decode_message(input_data)
print("Decoded Message:", decoded)


print(f"Execution Time = {time.time() - start_time:.5f}s")
