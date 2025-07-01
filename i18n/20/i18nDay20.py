"""i18n Puzzles - Puzzle 20
Solution Started: Jun 19, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/20
Solution by: Abbas Moosajee
Brief: [The future of Unicode]
"""

#!/usr/bin/env python3

import os, re, copy, time, base64
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

    def get_utf_text(self, encoded_message):
        bytes_data = base64.b64decode(encoded_message)
        encoding_type, stripped_bytes = self.__identify_encoding(bytes_data)
        utf_text = stripped_bytes.decode(encoding_type)

        if self.debug:
            print("   Init Message:", encoded_message)
            print("  Decoded bytes:", bytes_data)
            print("  Encoding Type:", encoding_type)
            print("  Bytes w/o BOM:", stripped_bytes)
            print("   Decoded text:", utf_text)
        return utf_text

    def regroup_utf16(self, utf16_text, n):
        regrouped_bits = ''
        for char in utf16_text:
            bits = f"{ord(char):0{n}b}"  # Binary string of length `n`, zero-padded
            # Strip leading 8 bits if they are all zeros (i.e., high byte is 0)
            stripped = bits[8:] if bits.startswith('00000000') else bits
            regrouped_bits += stripped

        # Split regrouped_bits into 8-bit chunks and convert each to an integer
        bit_list = [int(regrouped_bits[i:i+8], 2) for i in range(0, len(regrouped_bits), 8)]

        if self.debug:
            print(" Grouped Binary:", regrouped_bits)
            print("       Bit List:", bit_list)
        return bit_list

    @staticmethod
    def __add_bits(rem_bits, shift, start):
        """Construct a binary string starting from rem_bits[start], slicing off the last `shift` bits,
        then appending the last 6 bits of each remaining item."""
        bits = format(rem_bits[start], '08b')[-shift:]
        bits += ''.join(format(b, '08b')[-6:] for b in rem_bits[start + 1:])
        return bits

    def decode_binary(self, bits_list, k):
        """Decode a list of byte values into a binary string based on prefix rules."""
        decoded_bits = ''

        while bits_list:
            base = bits_list[0]

            if base >= 252:
                # 6-byte pattern (e.g., UTF-8 encoding for code points >= 0x4000000)
                chunk, bits_list = bits_list[:6], bits_list[6:]
                decoded_bits += self.__add_bits(chunk, shift=4, start=1)

            elif 248 <= base <= 251:
                # 5-byte pattern
                chunk, bits_list = bits_list[:5], bits_list[5:]
                decoded_bits += self.__add_bits(chunk, shift=2, start=0).zfill(k)

            elif 194 <= base <= 223:
                # 2-byte pattern (common for extended ASCII / multibyte UTF-8)
                chunk, bits_list = bits_list[:2], bits_list[2:]
                decoded_bits += self.__add_bits(chunk, shift=2, start=0).zfill(8)

            else:
                # Skip unrecognized or single-byte base characters
                bits_list = bits_list[1:]

        return decoded_bits

    def convert_to_utf8(self, binary_code):
        # Convert the binary string into bytes, 8 bits at a time
        bit_values = [int(binary_code[i:i+8], 2) for i in range(0, len(binary_code), 8)]
        byte_values = bytes(bit_values)
        message = byte_values.decode('utf-8')
        if self.debug:
            print(" Decoded Binary:", binary_code)
            print("     UTF-8 Bits:", bit_values)
            print("    UTF-8 Bytes:", byte_values)
            print("  Final Message:", message)
        return message

    def follow_message(self, message):
        # Extract all integers from the message
        numbers = list(map(int, re.findall(r'\d+', message)))

        # Sanity check: ensure there are exactly 3 numbers
        if len(numbers) != 3:
            raise ValueError("Expected exactly three numbers in the message.")

        # Return the number that is neither the min nor the max
        return sorted(numbers)[1]

    def decode_message(self, encrypted = None):
        if encrypted is None:
            encrypted = self.test_message
        joined_message = ''.join(encrypted)
        utf_text = self.get_utf_text(joined_message)
        utf8_bits = self.regroup_utf16(utf_text, n = 20)
        decoded_bits = self.decode_binary(utf8_bits, k = 28)
        message = self.convert_to_utf8(decoded_bits)
        value = self.follow_message(message)
        return message, value

decoded, result = UnicodeEncryptor().decode_message(input_data)
print("Decoded Message:", decoded)
print("     Final Code:", result)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
