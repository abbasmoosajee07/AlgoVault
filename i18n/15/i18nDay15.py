"""i18n Puzzles - Puzzle 15
Solution Started: May 22, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/15
Solution by: Abbas Moosajee
Brief: [24/5 Support]
"""

#!/usr/bin/env python3

import os, re, copy
import time as time1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta, time, timezone
from zoneinfo import ZoneInfo
from dateutil import tz  # only needed for UTC conversion formatting

start_time = time1.time()

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    offices, customers = [data_set.split('\n') for data_set in input_data]

class OfficeCalendar:
    def __init__(self, all_offices, customers):
        self.global_offices, self.customers = all_offices, customers
        # 0:00 UTC on Jan 1 2022, up to 24:00 UTC on Dec 31 2022
        YEAR_START, YEAR_END = ("2022-01-01 00:00 UTC", "2022-12-31 24:00 UTC")
        WORKING_HOURS = ("08:30", "17:30")
        WORKING_HOURS = "Monday to Friday, from 08:30 to 17:00"
        self.__build_timeset(2022)
        for office in all_offices:
            self.parse_office(office.split("	"))

    def __timestamp_to_datetime(self, timestamp: int, tz_name: str) -> datetime:
        if tz_name.upper() == "UTC":
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        else:
            return datetime.fromtimestamp(timestamp, tz=ZoneInfo(tz_name))

    def __build_timeset(self, YEAR):
        start = int(datetime(YEAR, 1, 1).timestamp())
        end = int(datetime(YEAR + 1, 1, 1).timestamp())

        timestamps = set(range(start, end, 60))  # step = 60 seconds
        timestamp = sorted(list(timestamps))[1]
        print(timestamp)

        dt_utc = datetime.fromtimestamp(timestamp, timezone.utc)
        print(dt_utc)  # 2025-01-01 00:00:00+00:00

        print("UTC: ", self.__timestamp_to_datetime(timestamp, "UTC"))
        print("Melbourne: ", self.__timestamp_to_datetime(timestamp, "Australia/Melbourne"))
        print("London: ", self.__timestamp_to_datetime(timestamp, "Europe/London"))

        return timestamps

    def __build_working_calendar(self, time_zone, holidays):
        start = int(datetime(2022, 1, 1).timestamp())
        end = int(datetime(2022 + 1, 1, 1).timestamp())

        timestamps = set(range(start, end, 60))  # step = 60 seconds
        timestamp = sorted(list(timestamps))[1]
        # print(timestamp)

        dt_utc = datetime.fromtimestamp(timestamp, timezone.utc)

        return timestamps

    def parse_office(self, office_info):
        print('  '.join(office_info))
        office_loc, time_zone, holidays = office_info
        office_loc = office_loc.split(" ")[-1]
        holidays = holidays.split(";")
        calendar = self.__build_working_calendar(time_zone, holidays)
        # print(office_loc, time_zone, holidays)
        return

    def parse_customer(self, customer_info):
        return

    def calculate_overtime(self):
        return 1

# calendar = OfficeCalendar(offices, customers)

# overtime_diff = calendar.calculate_overtime()
# print("Difference in Overtime:", overtime_diff)


def generate_timestamps(tz_name='America/New_York', holidays = []):
    # Setup
    weekday_map = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
        'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weekday_nums = {weekday_map[day] for day in weekdays}

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    start_time_str = '08:30'
    end_time_str = '17:00'
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    tz = ZoneInfo(tz_name)

    current = start_date.date()
    end = end_date.date()
    timestamps = []

    interval = timedelta(minutes=1)

    while current <= end:
        if current.weekday() in weekday_nums:
            # Combine once per day
            local_start = datetime.combine(current, start_time, tzinfo=tz)
            local_end = datetime.combine(current, end_time, tzinfo=tz)

            # Compute UTC offset once per day (fast DST handling)
            offset = local_start.utcoffset()
            utc_start = (local_start - offset).replace(tzinfo=None)
            num_minutes = int((local_end - local_start).total_seconds() // 60)

            # Fast loop, all naive UTC timestamps
            for i in range(num_minutes + 1):
                t = utc_start + i * interval
                ts = t.strftime("%Y-%m-%d %H:%M:%S+00:00")
                timestamps.append(ts)

        current += timedelta(days=1)

    return timestamps

timestamps = generate_timestamps()
print(len(timestamps))

print(f"Execution Time = {time1.time() - start_time:.5f}s")
