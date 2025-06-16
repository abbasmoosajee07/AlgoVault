# %%
"""i18n Puzzles - Puzzle 19
Solution Started: Jun 11, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/19
Solution by: Abbas Moosajee
Brief: [Out of date]
"""

#!/usr/bin/env python3

import os, re, copy, time, pytz, zoneinfo, tarfile
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
    SAVE_FOLDER = "tz_versions"
    LOG_FORMAT  = '%Y-%m-%dT%H:%M:%S%z'

    def download_tz_version(self, required_tz, debug=False):
        """Download and extract tzdata-<version>.tar.gz files from IANA"""
        tz_files = {}

        script_dir = os.path.dirname(os.path.abspath(__file__))
        tz_dir = os.path.join(script_dir, self.SAVE_FOLDER)
        self.tz_dir = tz_dir
        os.makedirs(tz_dir, exist_ok=True)
        print(tz_dir)

        for version in required_tz:
            filename = f"tzdata{version}.tar.gz"
            url = f"https://data.iana.org/time-zones/releases/{filename}"
            dest = os.path.join(tz_dir, filename)
            extract_dir = os.path.join(tz_dir, f"tzdata{version}")

            if not os.path.exists(dest):
                if debug:
                    print(f"Downloading {url}...")
                urllib.request.urlretrieve(url, dest)

            if not os.path.exists(extract_dir):
                if debug:
                    print(f"Extracting to {extract_dir}...")
                new_dir = os.makedirs(extract_dir, exist_ok=True)
                with tarfile.open(dest, "r:gz") as tar:
                    tar.extractall(path=extract_dir,numeric_owner=True)
                # print(extract_dir)


            # Compile time zone files
            zoneinfo_dir = extract_dir # os.path.join(tz_dir, f"zoneinfo_{version}")
            os.makedirs(zoneinfo_dir, exist_ok=True)
            os.system(f'zic -d "{zoneinfo_dir}" {extract_dir}/africa {extract_dir}/antarctica '
                      f'{extract_dir}/asia {extract_dir}/australasia {extract_dir}/etcetera '
                      f'{extract_dir}/europe {extract_dir}/northamerica {extract_dir}/southamerica')

            tz_files[version] = zoneinfo_dir

        return tz_files


    def correct_time_version(self, time_data, time_zone, version):
        shifted_set = set()
        # Extract Data
        timestamp = datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")
        tz_local = pytz.timezone(time_zone)

        local_dt = tz_local.localize(timestamp)  # timezone-aware
        dt_og = local_dt.astimezone(pytz.utc)    # converted to UTC

        # Inject the version-specific tzdata into zoneinfo
        version_dir = self.tz_files[version]
        # version_dir = os.path.abspath(version)
        # print(os.path.abspath(version))
        # print(version_dir)
        zoneinfo.ZoneInfo.clear_cache()
        zoneinfo.reset_tzpath([version_dir])
        timestamp = datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")

        # Recreate localized datetime with that version's tzinfo
        dt_new = timestamp.replace(tzinfo=tz_local)
        dt_new_utc = dt_new.astimezone(pytz.utc)

        # Compare the UTC time results
        if dt_og != dt_new_utc:
            shifted_set.add(version)

        # Format output as LOG_FORMAT
        dt_fmt = dt_new_utc.strftime('%Y-%m-%dT%H:%M:%S%z')
        dt_fmt = f"{dt_fmt[:-2]}:{dt_fmt[-2:]}"  # insert colon in UTC offset

        print(f"Version: {version}, {dt_new} Formatted: {dt_fmt}")

        return dt_fmt

    def identify_signal_time(self, signal_log, debug: bool = False):
        signal_list = [tuple(line.split('; ')) for line in signal_log]

        self.station_log = defaultdict(int)
        self.research_stations = set()
        self.tz_files = self.download_tz_version(self.TZ_VERSIONS)

        for time_data, time_zone in signal_list[:1]:
            for version in self.TZ_VERSIONS:
                print(f"UTC: {time_data} {time_zone}")
                corrected = self.correct_time_version(time_data, time_zone, version)
                self.station_log[corrected] += 1
        total_stations = len(self.research_stations)
        for stamp, count in self.station_log.items():
            print(stamp, count)
            if count == total_stations:
                print(stamp, "Valid")
        self.delete_tz()
        return len(signal_log)

    def delete_tz(self):
        import shutil
        # Delete the folder and all its contents
        shutil.rmtree(self.tz_dir)

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