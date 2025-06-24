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
import unicodedata, base64
from struct import unpack
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
            print("Decoded bytes:", bytes_data)
        self.encoding_type, stripped_bytes = self.__identify_encoding(bytes_data)
        if self.debug:
            print("Detected encoding:", self.encoding_type)
        # Decode to text
        utf16_text = stripped_bytes.decode(self.encoding_type)
        if self.debug:
            print("Stripped Bytes:", stripped_bytes)
            print("Decoded text:", utf16_text)
        return utf16_text, stripped_bytes

    def decode_utf16le_to_20bit_stream(self, raw: bytes):

        # Step 1: Decode as sequence of UTF-16LE code units (little endian)
        code_units = list(unpack(f'<{len(raw)//2}H', raw))

        # Step 2: Convert code units to 20-bit values
        bitstream = ""
        i = 0
        while i < len(code_units):
            cu = code_units[i]
            # Check for surrogate pair
            if 0xD800 <= cu <= 0xDBFF and i + 1 < len(code_units):
                next_cu = code_units[i + 1]
                if 0xDC00 <= next_cu <= 0xDFFF:
                    # Combine surrogate pair into 20-bit code point
                    codepoint = 0x10000 + ((cu - 0xD800) << 10) + (next_cu - 0xDC00)
                    bitstream += f'{codepoint:020b}'
                    i += 2
                    continue
            # Not a surrogate pair → just zero-extend the 16-bit value to 20 bits
            bitstream += f'{cu:020b}'
            i += 1

        # Step 3: Convert to hex representation
        bit_length = len(bitstream)
        hex_length = (bit_length + 3) // 4
        hex_string = hex(int(bitstream, 2))[2:]#.zfill(hex_length)

        return {
            'binary': bitstream,
            'hex': hex_string,
            'bits': bit_length,
            'chars': len(code_units)
        }

    def decode_message(self, encrypted):
        encrypted = self.test_message
        joined_message = ''.join(encrypted)
        if self.debug:
            print(len(joined_message), "Base64 string:", joined_message)
        utf16_text, utf16_bytes = self.__get_utf16(joined_message)
        print(utf16_bytes)
        result = self.decode_utf16le_to_20bit_stream(utf16_bytes)

        print("Total bits:", result['bits'])
        print("Binary:", result['binary'])
        print("Hex :", result['hex'])


        # regrouped = self.utf16_to_n_bit_groups(utf16_text, 20)
        # print(' '.join(regrouped))
        return

decoded = UnicodeEncryptor().decode_message(input_data)
print("Decoded Message:", decoded)


print(f"Execution Time = {time.time() - start_time:.5f}s")
