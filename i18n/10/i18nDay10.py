"""i18n Puzzles - Puzzle 10
Solution Started: Mar 16, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/10/
Solution by: Abbas Moosajee
Brief: [Unicode passwords strike back!]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt, unicodedata, functools

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n\n')

# Constructing the dictionary
AUTHENTICATIONS = {
    user: bcrypt_pwd
    for line in input_data[0].split('\n')  # Split input into lines
    for user, bcrypt_pwd in [line.split(' ', 1)]  # Split each line into (user, password)
}
login_attempts = input_data[1].split('\n')

def recompositions(normalized_string: str):
    nfc_chars = list(normalized_string)
    composed_indexes = {
        i for i, char in enumerate(nfc_chars)
        if char != unicodedata.normalize("NFD", char)
    }
    subsets_list = list(subsets(composed_indexes))
    return (
        "".join([
            unicodedata.normalize("NFD", char) if i in test_indexes else char
            for i, char in enumerate(nfc_chars)
        ])
        for test_indexes in subsets_list
    )

def subsets(superset):
    set_list = list(superset)
    return (
        {val for i, val in enumerate(set_list) if bitfield & (1 << i)}
        for bitfield in range(1 << len(set_list))
    )

@functools.lru_cache(maxsize=None)
def is_valid_login(normalized_attempt: str, hashed_pw: bytes) -> bool:
    return any(
        bcrypt.checkpw(test_pw.encode("utf-8"), hashed_pw)
        for test_pw in recompositions(normalized_attempt)
    )

def validate_login(username: str, password: str) -> bool:
    normalized = unicodedata.normalize("NFC", password)
    auth_password = AUTHENTICATIONS.get(username).encode("utf-8")
    if not auth_password:
        return False
    return is_valid_login(normalized, auth_password)

total_logins = 0
for login in login_attempts[:]:
    user, password = login.split(' ')
    valid_login = validate_login(user, password)
    if valid_login:
        total_logins += 1

print("Total Logins:", total_logins)
