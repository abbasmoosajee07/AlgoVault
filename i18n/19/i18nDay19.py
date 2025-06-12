"""i18n Puzzles - Puzzle 19
Solution Started: Jun 11, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/19
Solution by: Abbas Moosajee
Brief: [Out of date]
"""

#!/usr/bin/env python3

import os, re, copy, time, pytz
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import urllib.request
start_time = time.time()

# Load the input data from the specified file path
D19_file = "Day19_input1.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n')

class TimeLogger:
    TZ_VERSIONS = ('2018c', '2018g', '2021b', '2023d')
    LOG_FORMAT  = 'yyyy-mm-ddThh:mm:ss+00:00'

    def download_tz_version(self, required_tz):
        """Download tzdb-<version>.tar.lz.asc files from IANA to ./tz_versions/ folder"""
        tz_files = {}

        # Create subdirectory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        tz_dir = os.path.join(script_dir, "tz_versions")
        os.makedirs(tz_dir, exist_ok=True)

        for version in required_tz:
            filename = f"tzdb-{version}.tar.lz"  + '.asc'
            url = f"https://data.iana.org/time-zones/releases/{filename}"
            dest = os.path.join(tz_dir, filename)

            if not os.path.exists(dest):
                # print(f"⬇️ Downloading {filename}...")
                urllib.request.urlretrieve(url, dest)
            else:
                # print(f"📂 Already downloaded: {filename}")
                pass
            tz_files[version] = dest

        return tz_files

    def correct_time_record(self, signal):
        time_data, time_zone = signal.split('; ')
        tz_local = pytz.timezone(time_zone)
        strip_dt = datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")

        local_dt = tz_local.localize(strip_dt)  # Make it timezone-aware
        utc_dt = local_dt.astimezone(pytz.utc)  # Convert to UTC timezone

        # print(local_dt, utc_dt, tz_local)
        # self.research_stations.add(tz_local)
        self.station_log[time_zone] += 1
        return

    def identify_signal_time(self, signal_log, debug: bool = False):
        self.station_log = defaultdict(int)
        self.research_stations = set()
        self.tz_files = self.download_tz_version(self.TZ_VERSIONS)
        print(self.tz_files)
        for signal in signal_log:
            updated_time = self.correct_time_record(signal)
        total_stations = len(self.research_stations)
        return len(signal_log)

signal_timestamp = TimeLogger().identify_signal_time(input_data, True)
print("UTC Signal Timestamp:", signal_timestamp)


print(f"Execution Time = {time.time() - start_time:.5f}s")

# 2024-04-09 18:49:00; Africa/Casablanca converts to 2024-04-09T17:49:00+00:00.
# 2024-04-10 02:19:00; Asia/Pyongyang converts to 2024-04-09T17:49:00+00:00.
# 2024-04-10 04:49:00; Antarctica/Casey converts to 2024-04-09T17:49:00+00:00.
# 2024-04-12 12:13:00; Asia/Pyongyang converts to 2024-04-12T03:43:00+00:00.
# 2024-04-12 15:54:00; Africa/Casablanca converts to 2024-04-12T14:54:00+00:00.
# 2024-04-12 16:43:00; Africa/Casablanca converts to 2024-04-12T15:43:00+00:00.
# 2024-04-13 00:24:00; Asia/Pyongyang converts to 2024-04-12T15:54:00+00:00.
# 2024-04-13 01:54:00; Antarctica/Casey converts to 2024-04-12T14:54:00+00:00.
# 2024-04-13 07:43:00; Antarctica/Casey converts to 2024-04-12T20:43:00+00:00.

