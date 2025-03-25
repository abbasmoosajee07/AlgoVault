"""i18n Puzzles - Puzzle 9
Solution Started: Mar 16, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/9/
Solution by: Abbas Moosajee
Brief: [Nine Eleven]
"""

#!/usr/bin/env python3

import os, re, copy
import re, calendar, datetime

# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and sort input data into a grid
with open(D09_file_path) as file:
    input_data = file.read().strip().split('\n')

# Toggle between test and actual input
test_mode = False

def process_dates(lines):
    """Processes the input lines, extracting names with a known target date."""
    target_date = datetime.date(2001, 9, 11)
    people = extract_people_data(lines)
    matching_names = sorted(
        name for name, unknown_dates in people.items()
        if target_date in resolve_unknown_dates(unknown_dates)
    )
    print(" ".join(matching_names))

def extract_people_data(lines):
    """Reads input lines and maps names to their respective unknown dates."""
    people = {}
    for line in lines:
        unknown_date, names = parse_line(line)
        for name in names:
            people.setdefault(name, []).append(unknown_date)
    return people

def parse_line(line):
    """Parses a single line, extracting the date and associated names."""
    match = re.fullmatch(r"(\d+)-(\d+)-(\d+):\s*(?P<names>.*)", line)
    return (
        (int(match.group(1)), int(match.group(2)), int(match.group(3))),
        re.split(r",\s*", match.group("names"))
    )

def resolve_unknown_dates(unknown_dates):
    """Determines the actual dates from unknown formats, ensuring a unique format."""
    formats = determine_possible_formats(unknown_dates)
    if len(formats) != 1:
        raise ValueError(f"Multiple possible formats for {unknown_dates}: {formats}")
    chosen_format = next(iter(formats))
    return {
        convert_to_date(interprete_as_format(unknown_date, chosen_format))
        for unknown_date in unknown_dates
    }

def determine_possible_formats(unknown_dates):
    """Identifies all valid date formats for a given list of unknown dates."""
    potential_formats = {
        ("Y", "M", "D"),
        ("Y", "D", "M"),
        ("M", "D", "Y"),
        ("D", "M", "Y")
    }
    for unknown_date in unknown_dates:
        potential_formats -= {
            fmt for fmt in potential_formats if not is_valid_format(unknown_date, fmt)
        }
    return potential_formats

def is_valid_format(unknown_date, fmt):
    """Checks if the given format results in a valid calendar date."""
    year, month, day = interprete_as_format(unknown_date, fmt)
    return (
        0 <= year <= 99
        and 1 <= month <= 12
        and 1 <= day <= days_in_month(convert_full_year(year), month)
    )

def interprete_as_format(unknown_date, fmt):
    """Reorders date components based on the given format."""
    mapped = dict(zip(fmt, unknown_date))
    return (mapped["Y"], mapped["M"], mapped["D"])

def convert_to_date(date):
    """Converts a tuple representation of a date into a datetime.date object."""
    year, month, day = date
    return datetime.date(convert_full_year(year), month, day)

def convert_full_year(year):
    """Expands a two-digit year into a four-digit year based on cutoff."""
    return (2000 if year < 20 else 1900) + year

def days_in_month(year, month):
    """Returns the number of days in a given month of a specific year."""
    return calendar.monthrange(year, month)[1]

process_dates([line.strip() for line in input_data])