"""i18n Puzzles - Puzzle 7
Solution Started: Mar 13, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/7/
Solution by: Abbas Moosajee
Brief: [The audit trail fixer]
"""

#!/usr/bin/env python3

import os, datetime, zoneinfo

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split('\n')


def fix_audit_trail(input_data: str):
    halifax = zoneinfo.ZoneInfo("America/Halifax")
    santiago = zoneinfo.ZoneInfo("America/Santiago")

    total_shift = 0
    for index, time_stamp in enumerate(input_data, start = 1):
        timestamp, correct, incorrect = time_stamp.split('\t')

        # Parse timestamp (including the UTC offset)
        incorrect_time = datetime.datetime.fromisoformat(timestamp)

        # Convert to UTC before processing
        incorrect_time_utc = incorrect_time.astimezone(datetime.timezone.utc)

        # Apply correction
        corrected_time_utc = (
            incorrect_time_utc
            - datetime.timedelta(minutes=int(incorrect))
            + datetime.timedelta(minutes=int(correct))
        )

        # Determine the correct timezone
        target_tz = halifax if incorrect_time.utcoffset() == halifax.utcoffset(incorrect_time) else santiago

        # Convert to local timezone
        correct_time = corrected_time_utc.astimezone(target_tz)

        # Compute final result
        total_shift += correct_time.hour * index

    return total_shift

time_shifts = fix_audit_trail(input_data)

print("Total Time sum:", time_shifts)


