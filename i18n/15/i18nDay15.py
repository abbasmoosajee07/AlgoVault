"""i18n Puzzles - Puzzle 15
Solution Started: Mar 28, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/15/
Solution by: Abbas Moosajee
Brief: [24/5 support]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n\n')

class Office_Calendar:
    def __init__(self):
        YEAR_START = "2022-01-01 00:00 UTC"
        YEAR_END = "2022-12-31 24:00 UTC"
        WORKING_HOURS = "Monday to Friday, from 08:30 to 17:00"

    def create_schedule(self, all_offices: list[str]):
        schedule = 1
        for office in all_offices:
            _, office_tz, holidays = office.split('\t')
            holidays = holidays.split(';')
            print(office_tz, holidays)
        return schedule

global_offices, customers = [data_set.split('\n') for data_set in input_data]

toplap_calendar = Office_Calendar()
schedule_2022 = toplap_calendar.create_schedule(global_offices)

from datetime import datetime, timedelta
import pytz

# Office closures per timezone
office_closures = {
    "Australia/Melbourne": ["2022-12-26", "2022-04-15", "2022-04-18", "2022-01-26"],
    "Europe/Amsterdam": ["2022-06-06", "2022-12-26", "2022-05-26", "2022-04-27"],
    "Europe/London": ["2022-12-26", "2022-04-15", "2022-06-03"],
    "America/Sao_Paulo": ["2022-02-28", "2022-12-26", "2022-04-15", "2022-05-01"],
    "America/New_York": ["2022-01-17", "2022-12-26", "2022-07-04", "2022-09-05"]
}


# Define working hours in UTC
work_start_utc = "08:30"
work_end_utc = "17:00"
work_days = {0, 1, 2, 3, 4}  # Monday to Friday
weekends = {5, 6}  # Saturday and Sunday

def generate_hourly_calendar(year, office_closures):
    hourly_calendar = {}
    
    for office, closures in office_closures.items():
        tz = pytz.timezone(office)
        start_date = datetime(year, 1, 1, tzinfo=pytz.UTC)
        end_date = datetime(year, 12, 31, tzinfo=pytz.UTC)
        
        current_date = start_date
        while current_date <= end_date:
            local_date = current_date.astimezone(tz).date()
            local_date_str = local_date.strftime("%Y-%m-%d")
            
            utc_start = tz.localize(datetime.strptime(f"{local_date_str} {work_start_utc}", "%Y-%m-%d %H:%M")).astimezone(pytz.UTC)
            utc_end = tz.localize(datetime.strptime(f"{local_date_str} {work_end_utc}", "%Y-%m-%d %H:%M")).astimezone(pytz.UTC)
            
            if local_date_str not in hourly_calendar:
                hourly_calendar[local_date_str] = ["Cl " for _ in range(24)]
            
            if local_date.weekday() in work_days and local_date_str not in closures:
                start_hour = utc_start.hour
                end_hour = utc_end.hour
                
                for hour in range(start_hour, 24):
                    hourly_calendar[local_date_str][hour] = "Op "
                
                if end_hour < start_hour:  # Handle work shift crossing midnight
                    next_day = (local_date + timedelta(days=1)).strftime("%Y-%m-%d")
                    if next_day not in hourly_calendar:
                        hourly_calendar[next_day] = ["Cl " for _ in range(24)]
                    for hour in range(0, end_hour + 1):
                        hourly_calendar[next_day][hour] = "Op "
            
            current_date += timedelta(days=1)
    
    return hourly_calendar

# Generate the 2022 hourly calendar
hourly_calendar_2022 = generate_hourly_calendar(2022, office_closures)

# Print a sample in the desired format
print("\nHourly Availability in 2022:")
for date, hours in list(hourly_calendar_2022.items())[99:102]:  # Print first 10 days
    hour_labels = " ".join([str(h).zfill(2) for h in range(24)])
    open_closed = "".join(hours)
    print(f"{date}   {hour_labels}\n{' ' * 12} {open_closed}\n")
