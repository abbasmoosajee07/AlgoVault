"""i18n Puzzles - Puzzle 8
Solution Started: Mar 14, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/8/
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, unicodedata

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n')

def normalize_letter(c):
    """Normalize a character to remove accents and convert to lowercase."""
    normalized = unicodedata.normalize('NFKD', c)  # Decomposes accents (e.g., Á → A´)
    return ''.join([ch for ch in normalized if unicodedata.category(ch) != 'Mn']).lower()

def normalize_letter(c):
    """Normalize a character by removing accents and converting it to lowercase."""
    normalized = unicodedata.normalize('NFKD', c)
    return ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn').lower()

def is_valid_password(password, verbose=False):
    """Check if the password meets all validity rules, with optional visualization."""

    # Length check
    if not (4 <= len(password) <= 12):
        if verbose:
            print(f"❌ Invalid: {password} (wrong length)")
        return False

    # At least one digit
    if not any(c.isdigit() for c in password):
        if verbose:
            print(f"❌ Invalid: {password} (no digit)")
        return False

    vowels = set("aeiouáéíóúäëïöüàèìòùâêîôûãõ")
    consonants = set("bcdfghjklmnpqrstvwxyzñŷç")

    has_vowel = has_consonant = False
    seen = set()
    prev_normalized = None  # Track for immediate duplicates

    for c in password:
        norm_c = normalize_letter(c)  # Remove accents, lowercase

        # Check for vowels and consonants
        if norm_c in vowels:
            has_vowel = True
        elif norm_c in consonants:
            has_consonant = True

        # Detect consecutive or duplicate letters
        if norm_c == prev_normalized:
            if verbose:
                print(f"❌ Invalid: {password} (double letter '{c}')")
            return False

        if norm_c in seen:
            if verbose:
                print(f"❌ Invalid: {password} (repeated letter '{c}')")
            return False

        seen.add(norm_c)
        prev_normalized = norm_c  # Update last seen letter

    # Final vowel and consonant check
    if not has_vowel:
        if verbose:
            print(f"❌ Invalid: {password} (missing vowel)")
        return False
    if not has_consonant:
        if verbose:
            print(f"❌ Invalid: {password} (missing consonant)")
        return False

    if verbose:
        print(f"✅ Valid: {password}")
    return True

# Example usage
valid_passwords = [pw for pw in input_data if is_valid_password(pw)]

print("Total Valid Passwords:", len(valid_passwords))
