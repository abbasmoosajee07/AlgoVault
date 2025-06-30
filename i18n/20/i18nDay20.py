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
        self.test_decoded = "ꪪꪪꪪ This is a secret message. ꪪꪪꪪ Good luck decoding me! ꪪꪪꪪ"

    def __get_test(self, file_name):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        with open(test_file) as file:
            input_data = file.read().strip().split('\n')
        return input_data

    def __identify_encoding(self, bytes_data):
        """Identify Encoding and  remove BOM"""
        if bytes_data.startswith(b'\xff\xfe'):
            return "utf-16-le", bytes_data[2:]
        elif bytes_data.startswith(b'\xfe\xff'):
            return "utf-16-be", bytes_data[2:]
        elif bytes_data.startswith(b'\xef\xbb\xbf'):
            return "utf-8-sig", bytes_data[3:]  # UTF-8 BOM is 3 bytes
        else:
            return "utf-8", bytes_data  # Default fallback

    def __get_utf_text(self, encoded_message):
        bytes_data = base64.b64decode(encoded_message)
        encoding_type, stripped_bytes = self.__identify_encoding(bytes_data)
        utf_text = stripped_bytes.decode(encoding_type)

        if self.debug:
            print(" Init Message:", encoded_message)
            print("Decoded bytes:", bytes_data)
            print("Encoding Type:", encoding_type)
            print("Bytes w/o BOM:", stripped_bytes)
            print(" Decoded text:", utf_text)
        return utf_text

    def __regroup_utf16(self, utf16_text, n):
        regrouped_bits = ''
        for char in utf16_text:
            bits = f"{ord(char):0{n}b}"  # Binary string of length `n`, zero-padded
            # Strip leading 8 bits if they are all zeros (i.e., high byte is 0)
            stripped = bits[8:] if bits.startswith('00000000') else bits
            regrouped_bits += stripped

        # Split regrouped_bits into 8-bit chunks and convert each to an integer
        bit_list = [int(regrouped_bits[i:i+8], 2) for i in range(0, len(regrouped_bits), 8)]

        if self.debug:
            print(" Grouped Bits:", regrouped_bits)
            print("     Bit List:", bit_list)
        return bit_list

    def decode_message(self, encrypted):
        encrypted = self.test_message
        joined_message = ''.join(encrypted)
        self.debug = True
        utf_text = self.__get_utf_text(joined_message)
        utf8_bits = self.__regroup_utf16(utf_text, 20)

        return

decoded = UnicodeEncryptor().decode_message(input_data)
print("Decoded Message:", decoded)


print(f"Execution Time = {time.time() - start_time:.5f}s")
