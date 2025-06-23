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
import unicodedata, base64, binascii
start_time = time.time()

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')

class UnicodeEncryptor:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.test_message = self.__get_test("test_input.txt")
        self.decoded_test = "ꪪꪪꪪ This is a secret message. ꪪꪪꪪ Good luck decoding me! ꪪꪪꪪ"

    def __get_test(self, file_name):
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        with open(test_file) as file:
            input_data = file.read().strip().split('\n')
        return input_data

    def __identify_encoding(self, bytes_data):
        if bytes_data.startswith(b'\xff\xfe'):
            return "utf-16-le", bytes_data[2:]
        elif bytes_data.startswith(b'\xfe\xff'):
            return "utf-16-be", bytes_data[2:]
        elif bytes_data.startswith(b'\xef\xbb\xbf'):
            return "utf-8-sig", bytes_data[3:]  # UTF-8 BOM is 3 bytes
        else:
            return "utf-8", bytes_data  # Default fallback

    def __get_utf16(self, encoded_message):
        bytes_data = base64.b64decode(encoded_message)
        if self.debug:
            print(len(bytes_data), "Decoded bytes:", bytes_data)
        self.encoding_type, stripped_bytes = self.__identify_encoding(bytes_data)
        if self.debug:
            print("Detected encoding:", self.encoding_type)
        # Decode to text
        utf16_text = stripped_bytes.decode(self.encoding_type)
        if self.debug:
            print(len(stripped_bytes), "Stripped Bytes:", stripped_bytes)
            print(len(utf16_text), "Decoded text:", utf16_text)
        return utf16_text, stripped_bytes

    def utf16_to_n_bit_groups(self, text, n):
        # Step 1: Convert each character to its Unicode code point
        codepoints = [ord(c) for c in text]
        # for byte_char in text:
        #     print(byte_char, ord(byte_char))
        print(codepoints)
        # Step 2: Convert each code point to binary string (padded to 16+ bits)
        bin_string = [f'{cp:020b}' for cp in codepoints]
        bin_string = ''.join(bin_string)
        print(bin_string)
        # Step 3: Group into n-bit chunks
        grouped = [bin_string[i:i+n] for i in range(0, len(bin_string), n)]

        return grouped

    def decode_message(self, encrypted):
        encrypted = self.test_message
        joined_message = ''.join(encrypted)
        if self.debug:
            print(len(joined_message), "Base64 string:", joined_message)
        utf16_text, utf16_bytes = self.__get_utf16(joined_message)
        new_line = ''
        for byte_char in utf16_bytes:
            new_line += chr(byte_char)
            print(byte_char,new_line[-1], ord(chr(byte_char)))
        self.debug = True
        print(new_line)
        regrouped = self.utf16_to_n_bit_groups(utf16_text, 20)
        print(' '.join(regrouped))
        return

decoded = UnicodeEncryptor().decode_message(input_data)
print("Decoded Message:", decoded)

print(f"Execution Time = {time.time() - start_time:.5f}s")
