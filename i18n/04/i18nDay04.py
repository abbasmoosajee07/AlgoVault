"""i18n Puzzles - Puzzle 4
Solution Started: Mar 10, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/4/
Solution by: Abbas Moosajee
Brief: [A trip around the world]
"""

#!/usr/bin/env python3

import os, re, copy
from datetime import datetime
from zoneinfo import ZoneInfo  # Built-in since Python 3.9

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n\n')


def extract_datetime(text):
    """Extracts date, time, and timezone from a given string and returns a timezone-aware datetime."""
    match = re.search(r"[A-Za-z]+:\s+([\w/\-]+)\s+([A-Za-z]{3} \d{2}, \d{4}), (\d{2}:\d{2})", text)
    if match:
        tz_str, date_part, time_part = match.groups()
        dt_naive = datetime.strptime(f"{date_part} {time_part}", "%b %d, %Y %H:%M")

        try:
            return dt_naive.replace(tzinfo=ZoneInfo(tz_str))
        except ValueError:
            raise ValueError(f"Unknown timezone: {tz_str}")

    raise ValueError("Invalid datetime format")

def calculate_travel_time(departure: str, arrival: str) -> int:
    """Calculates travel time in minutes between two timezone-aware datetime strings."""
    dep_time = extract_datetime(departure)
    arv_time = extract_datetime(arrival)

    # Convert both to UTC before calculating the difference
    time_difference = arv_time.astimezone(ZoneInfo("UTC")) - dep_time.astimezone(ZoneInfo("UTC"))

    return int(time_difference.total_seconds() / 60)

total_travel = 0
for trip in input_data:
    dep, arv = trip.split('\n')
    trip_time = calculate_travel_time(dep, arv)
    total_travel += trip_time

    # print(dep, '\n', arv, sep="")
    # print(f"{trip_time=} {total_travel=}")

print("Total Travel Time:", total_travel)