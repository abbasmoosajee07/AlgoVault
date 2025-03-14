"""i18n Puzzles - Puzzle 8
Solution Started: Mar 14, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/8/
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n')

test_input = ['iS0', 'V8AeC1S7KhP4Ļu', 'pD9Ĉ*jXh', 'E1-0', 'ĕnz2cymE', 'tqd~üō', 'IgwQúPtd9', 'k2lp79ąqV']
import unicodedata

def normalize_letter(c):
    """Normalize a character to remove accents and convert to lowercase."""
    normalized = unicodedata.normalize('NFKD', c)  # Decomposes accents (e.g., Á → A´)
    return ''.join([ch for ch in normalized if unicodedata.category(ch) != 'Mn']).lower()

def is_valid_password(password):
    """Check if the password meets all validity rules."""
    if not (4 <= len(password) <= 12):  # Length check
        print("wrong length:", password)
        return False

    if not any(c.isdigit() for c in password):  # At least one digit
        print("no digit:", password)
        return False

    vowels = set("aeiouáéíóúäëïöüàèìòùâêîôûãõ")
    consonants = set("bcdfghjklmnpqrstvwxyzñŷç")  # Including special consonants

    has_vowel = any(c in vowels for c in password)
    has_consonant = any(c in consonants for c in password)

    if not has_vowel:  # Must contain at least one vowel and one consonant
        print("has vowel:", password)
        return False

    if not has_consonant:
        print("has consonant:", password)
        return False

    # Check for duplicate letters (ignoring accents and case)
    seen = set()
    for c in password:
        normalized_c = normalize_letter(c)  # Remove accents, lowercase
        if normalized_c in seen:
            
            return False  # Duplicate found
        seen.add(normalized_c)

    return True

# Validate passwords from input_data
valid_passwords = [password for password in test_input if is_valid_password(password)]

print("No. of Valid Passwords:", len(valid_passwords))

