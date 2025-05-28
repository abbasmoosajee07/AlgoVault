"""i18n Puzzles - Puzzle 15
Solution Started: May 22, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/15
Solution by: Abbas Moosajee
Brief: [24/5 Support]
"""

#!/usr/bin/env python3

import os, re, copy, time, pytz
from datetime import datetime, timedelta, timezone
start_time = time.time()

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path, encoding="utf-8") as file:
    input_data = file.read().strip().split('\n\n')
    offices, customers = [data_set.split('\n') for data_set in input_data]

class OfficeCalendar:
    def __init__(self, all_offices, all_customers, target_year = 2022):
        self.YEAR = target_year

        weekday_map = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
            'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.weekday_nums = {weekday_map[day] for day in weekdays}

        self.office_calendar = self.__parse_calendar_schedule(all_offices, "08:30-17:00")
        self.customer_calendar = self.__parse_calendar_schedule(all_customers, "00:00-24:00")

    def __parse_calendar_schedule(self, all_data, working_hours ):
        full_calendar = {}
        for line in all_data[:]:
            location, time_zone, holidays = line.split("\t")
            calendar = self.__build_working_calendar(time_zone, holidays.split(";"), working_hours)
            corrected_loc = ' '.join(location.split()[-3:])
            full_calendar[corrected_loc] = calendar
        return full_calendar

    def __build_working_calendar(self, time_zone, holidays, working_hours):
        output = set()
        tz_local = pytz.timezone(time_zone)
        converted_holidays = {datetime.strptime(h, '%d %B %Y').date() for h in holidays}

        start_date = datetime(self.YEAR, 1, 1)
        end_date = datetime(self.YEAR, 12, 31) + timedelta(days=1)

        # Build date list like get_coverage
        base_utc = pytz.utc.localize(start_date)
        ymd_to_use = [(d.year, d.month, d.day) for d in
                (start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1))]
        ymd_to_use += [(self.YEAR - 1, 12, 31)]

        for year, month, day in ymd_to_use:
            try:
                date = datetime(year, month, day)
            except ValueError:
                continue  # Skip invalid dates like April 31

            if date.weekday() in self.weekday_nums and date.date() not in converted_holidays:
                work_start_str, work_end_str = working_hours.split('-')
                local_start = datetime.combine(date, datetime.strptime(work_start_str, "%H:%M").time())
                if work_end_str == "24:00":
                    local_end = date + timedelta(days=1)
                else:
                    local_end = datetime.combine(date, datetime.strptime(work_end_str, "%H:%M").time())
                # Localize start and end
                local_start_tz = tz_local.localize(local_start)
                local_end_tz = tz_local.localize(local_end)

                # Calculate offset from base UTC in seconds
                start_delta = local_start_tz - base_utc
                end_delta = local_end_tz - base_utc

                start_block = int(start_delta.total_seconds()) // (60 * 30)
                end_block = int(end_delta.total_seconds()) // (60 * 30)

                # Inclusive start, exclusive end range
                output |= set(range(start_block, end_block))


        # Limit output to valid range (like in get_coverage)
        min_output = 0
        max_output = int((end_date- start_date).total_seconds()) // (60 * 30)
        output = {num for num in output if num in range(min_output, max_output)}
        return output

    def visualize_day(self, day: datetime):
        paper = []
        mins_block = 30
        base_utc = datetime(self.YEAR, 1, 1, tzinfo=timezone.utc)
        day_start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
        block_start_index = int((day_start - base_utc).total_seconds()) // (60 * mins_block)

        hour_blocks = list(range(25))  # 0 to 23

        def get_hour_row(calendar, symbol):
            row = ""
            for hour in hour_blocks:
                # Each hour spans 2 blocks: hour*2 and hour*2 + 1
                block_indices = [block_start_index + hour * 2, block_start_index + hour * 2 + 1]
                active = any(b in calendar for b in block_indices)
                row += symbol if active else " _"
            return row

        first_digits = "".join(f"{h//10} " for h in hour_blocks)
        second_digits = "".join(f"{h%10} " for h in hour_blocks)

        day_name = day.strftime('%A')
        date_label = day.strftime('%d-%m-%Y')

        paper.append(f"{day_name:<15}Hour (UTC): {first_digits}")
        paper.append(f"{date_label:<15}            {second_digits}")

        for loc, cal in self.office_calendar.items():
            row = get_hour_row(cal, " S")
            paper.append(f"{loc:>25}:{row}")
        paper.append(" " * len(paper[1]))
        for loc, cal in self.customer_calendar.items():
            row = get_hour_row(cal, " R")
            paper.append(f"{loc:>25}:{row}")

        print('\n'.join(paper))
        return paper

    def calculate_overtime(self):
        all_global_offices = set.union(*self.office_calendar.values())
        self.office_calendar["All Offices"] = all_global_offices
        overtime = [len(customer_cal | all_global_offices) * 30 \
                for customer_cal in self.customer_calendar.values()]

        return max(overtime) - min(overtime)

calendar = OfficeCalendar(offices, customers, 2022)

overtime_diff = calendar.calculate_overtime()
print("Difference in Overtime:", overtime_diff)

# To visualize a day, in UTC time:
# year, month, day = (2022, 4, 11)
# year, month, day = (2022, 12, 9)
# year, month, day = (2022, 4, 18)
# test_date = datetime(year, month, day)
# calendar.visualize_day(test_date + timedelta(days=0))

print(f"Execution Time = {time.time() - start_time:.5f}s")
