"""i18n Puzzles - Puzzle 2
Solution Started: Mar 8, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/2/
Solution by: Abbas Moosajee
Brief: [Detecting gravitational waves]
"""

#!/usr/bin/env python3

import os
import pandas as pd
from collections import Counter

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split('\n')

def convert_to_utc_series(timestamp_series):
    """Convert a Pandas Series of timestamps with mixed time zones to UTC."""
    timestamp_series = pd.Series(timestamp_series)  # Ensure it's a Series
    return pd.to_datetime(timestamp_series, utc=True).dt.tz_convert("UTC").astype(str)

# Convert input timestamps to UTC
utc_timestamps = convert_to_utc_series(input_data)

# Count occurrences efficiently using Counter
time_counts = Counter(utc_timestamps)

# Find the first time with exactly 4 occurrences
target_time = next(time for time, count in time_counts.items() if count == 4)

print("Target Time:", target_time)
