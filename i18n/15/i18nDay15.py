"""i18n Puzzles - Puzzle 15
Solution Started: May 22, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/15
Solution by: Abbas Moosajee
Brief: [24/5 Support]
"""

#!/usr/bin/env python3

import os, re, copy
import time as bench_time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta, time, timezone
from zoneinfo import ZoneInfo
from dateutil import tz  # only needed for UTC conversion formatting

start_time = bench_time.time()

# Load the input data from the specified file path
D15_file = "Day15_input1.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    offices, customers = [data_set.split('\n') for data_set in input_data]

class OfficeCalendar:
    def __init__(self, all_offices, all_customers):
        self.global_offices = all_offices
        self.customers = all_customers
        self.count = 0
        self.BASE_TIMESET = self.__build_timeset(2022)

        weekday_map = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
            'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.weekday_nums = {weekday_map[day] for day in weekdays}

        self.start_date = datetime(2022, 1, 1)
        self.end_date = datetime(2022, 12, 31)
        self.office_calendar = self.parse_calendar_schedule(all_offices, "08:30-17:00")

        year, month, day = (2022, 4, 11)
        # year, month, day = (2022, 12, 9)
        year, month, day = (2022, 4, 18)
        self.start_date = datetime(year, month, day)
        self.end_date =  self.start_date
        self.customer_calendar = self.parse_calendar_schedule(all_customers, "00:00-24:00")

        print("Offices parsed:", self.count)

    def __timestamp_to_datetime(self, timestamp: int, tz_name: str = "UTC") -> datetime:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc if tz_name.upper() == "UTC" else ZoneInfo(tz_name))

    def __build_timeset(self, year):
        start = int(datetime(year, 1, 1).timestamp())
        end = int(datetime(year + 1, 1, 1).timestamp())
        return set(range(start, end, 60))  # 1-minute granularity

    def __build_working_calendar(self, time_zone, holidays, working_hours):
        self.count += 1
        work_start, work_end = working_hours.split('-')
        start_date = self.start_date
        end_date =  self.end_date

        if work_end == "24:00":
            work_end = "23:59"
            # work_end = "00:00"
            # end_date = start_date + timedelta(days=1)
        # print(start_date, work_start, end_date, work_end)

        work_start = datetime.strptime(work_start, "%H:%M").time()
        work_end = datetime.strptime(work_end, "%H:%M").time()
        converted_holidays = [datetime.strptime(date_str, '%d %B %Y').strftime('%Y-%m-%d') for date_str in holidays]
        tz_local = ZoneInfo(time_zone)
        timestamps = set()

        current_date = start_date.date()
        while current_date <= end_date.date():
            # print(type(current_date))
            if f"{current_date}" in converted_holidays:
                pass
            elif datetime.combine(current_date, time.min).weekday() in self.weekday_nums:
                # Define local start and end datetime for the workday
                start_dt_local = datetime.combine(current_date, work_start, tzinfo=tz_local)
                end_dt_local = datetime.combine(current_date, work_end, tzinfo=tz_local)

                # Convert to UTC
                start_dt_utc = start_dt_local.astimezone(tz.UTC)
                end_dt_utc = end_dt_local.astimezone(tz.UTC)

                # Compute timestamp range in seconds (1-minute steps)
                start_ts = int(start_dt_utc.timestamp())
                end_ts = int(end_dt_utc.timestamp())

                # Add 1-minute interval timestamps to the set
                timestamps.update(range(start_ts, end_ts + 0, 60))

            current_date += timedelta(days=1)
        # call = 0
        # test = list(sorted(timestamps))[call]
        # print(time_zone, self.__timestamp_to_datetime(test, time_zone), self.__timestamp_to_datetime(test))
        return timestamps

    def parse_calendar_schedule(self, all_data, working_hours):
        full_calendar = {}
        for line in all_data[:]:
            line_info = line.split("\t")
            location, time_zone, holidays = line_info
            holidays = holidays.split(";")
            calendar = self.__build_working_calendar(time_zone, holidays, working_hours)
            corrected_loc = location.split()[-3:]# location.replace("TOPlap","")
            full_calendar[' '.join(corrected_loc)] = calendar
            # print("Working minutes in calendar:", len(calendar))
        return full_calendar

    def visualize_day(self, day: datetime):

        day_start = int(datetime(day.year, day.month, day.day, 0, 0, tzinfo=timezone.utc).timestamp())
        hour_blocks = list(range(25))  # 0 to 24

        def get_hour_row(calendar, symbol):
            row = ""
            for hour in hour_blocks:
                hour_start = day_start + hour * 3600
                hour_end = hour_start + 3599
                active = any(ts in calendar for ts in range(hour_start, hour_end + 1, 60))
                row += symbol if active else " _"
            return row

        # Header with split hour digits
        first_digits = "".join(f"{h//10} " for h in hour_blocks)
        second_digits = "".join(f"{h%10} " for h in hour_blocks)

        day_name = day.strftime('%A')
        date_label = day.strftime('%d %B %Y')

        print(f"{day_name:<15}Hour (UTC): {first_digits}")
        print(f"{date_label:<15}            {second_digits}")

        for loc, cal in self.office_calendar.items():
            row = get_hour_row(cal, " S")
            print(f"{loc:>25} {row}")
        for loc, cal in self.customer_calendar.items():
            row = get_hour_row(cal, " R")
            print(f"{loc:>25} {row}")

    def calculate_overtime(self):
        all_global_offices = set()
        for office_loc, calendar in self.office_calendar.items():
            all_global_offices.update(calendar)
        print(len(all_global_offices))
        overtime = []
        total_overtime = set()
        for customer_loc, customer_cal in self.customer_calendar.items():
            office_copy = all_global_offices.copy()
            diff =  customer_cal - office_copy
            total_overtime.update(diff)
            print(customer_loc, len(customer_cal) / 60, len(diff))
            overtime.append(len(diff))
        # print(len(total_overtime))
        self.visualize_day(self.start_date)

        return max(overtime) - min(overtime)


calendar = OfficeCalendar(offices, customers)

overtime_diff = calendar.calculate_overtime()
print("Difference in Overtime:", overtime_diff)

print(f"Execution Time = {bench_time.time() - start_time:.5f}s")

# Monday                  Hour (UTC): 0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 #
# 11 April 2022                                           0 1 2 3 4 5 6 7 8 9 0 1 2 3 #
#                                     | | | | | | | | | | | | | | | | | | | | | | | | #
#                           Melbourne SSSSSSSSSSSSSS                               SSS#
#                               Delft              SSSSSSSSSSSSSSSSS                  #
#                          Manchester                SSSSSSSSSSSSSSSSS                #
#                           São Paulo                        SSSSSSSSSSSSSSSSS        #
#                             Orlando                          SSSSSSSSSSSSSSSSS      #
#                                     | | | | | | | | | | | | | | | | | | | | | | | | #
#                  FaxSchool, Halifax       RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#
#    El Universidad Libre de Santiago         RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#
#                    Tokyo Media Corp RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#


# Friday                  Hour (UTC): 0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 #
# 09 December 2022                                        0 1 2 3 4 5 6 7 8 9 0 1 2 3 #
#                                     | | | | | | | | | | | | | | | | | | | | | | | | #
#                           Melbourne SSSSSSSSSSSS                                    #
#                               Delft                SSSSSSSSSSSSSSSSS                #
#                          Manchester                  SSSSSSSSSSSSSSSSS              #
#                           São Paulo                        SSSSSSSSSSSSSSSSS        #
#                             Orlando                            SSSSSSSSSSSSSSSSS    #
#                                     | | | | | | | | | | | | | | | | | | | | | | | | #
#                  FaxSchool, Halifax RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#
#    El Universidad Libre de Santiago RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#
#                    Tokyo Media Corp RRRRRRRRRRRRRRRRRRRRRRRRRRRRRR                  #

# Monday                  Hour (UTC): 0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 #
# 18 April 2022                                           0 1 2 3 4 5 6 7 8 9 0 1 2 3 #
#                                     | | | | | | | | | | | | | | | | | | | | | | | | #
#                           Melbourne                                              SSS#
#                               Delft              SSSSSSSSSSSSSSSSS                  #
#                          Manchester                SSSSSSSSSSSSSSSSS                #
#                           São Paulo                        SSSSSSSSSSSSSSSSS        #
#                             Orlando                          SSSSSSSSSSSSSSSSS      #
#                                     | | | | | | | | | | | | | | | | | | | | | | | | #
#                  FaxSchool, Halifax       RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#
#    El Universidad Libre de Santiago                                                 #
#                    Tokyo Media Corp RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR#

# FaxSchool, Halifax requires 41730 minutes of overtime.
# El Universidad Libre de Santiago requires 41820 minutes of overtime
# Tokyo Media Corp requires 44760 minutes of overtime.
# In this case: 44760-41730 = 3030 minutes.