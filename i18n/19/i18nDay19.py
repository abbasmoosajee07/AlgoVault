# %%
"""i18n Puzzles - Puzzle 19
Solution Started: Jun 11, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/19
Solution by: Abbas Moosajee
Brief: [Out of date]
"""

#!/usr/bin/env python3

import os, re, copy, time, zoneinfo
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, reset_tzpath, TZPATH
import urllib.request, tarfile
start_time = time.time()

# Load the input data from the specified file path
D19_file = "Day19_input1.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n')

class TimeLogger:
    TZ_VERSIONS = ('2018c', '2018g', '2021b', '2023d')
    # TZ_VERSIONS = ['2025b', '2024b']
    LOG_FORMAT  = '%Y-%m-%dT%H:%M:%S%z'

    @staticmethod
    def get_tz_files(required_tz, tz_folder = "tz_versions"):
        """Download and extract tzdata-<version>.tar.gz files from IANA"""
        tz_files = {}

        script_dir = os.path.dirname(os.path.abspath(__file__))
        tz_dir = os.path.join(script_dir, tz_folder)
        os.makedirs(tz_dir, exist_ok=True)

        for version in required_tz:
            filename = f"tzdb-{version}.tar.lz"
            filename = f"tzdata{version}.tar.gz"
            url = f"https://data.iana.org/time-zones/releases/{filename}"
            dest = os.path.join(tz_dir, filename)
            extract_dir = os.path.join(tz_dir, f"tzdata{version}")

            if not os.path.exists(dest):
                urllib.request.urlretrieve(url, dest)

            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir, exist_ok=True)
                with tarfile.open(dest, "r:gz") as tar:
                    tar.extractall(path=extract_dir, filter="tar")
            # # Compile time zone files
            # zoneinfo_dir = extract_dir# os.path.join(tz_dir, f"tz_{version}")
            # os.makedirs(zoneinfo_dir, exist_ok=True)
            # os.system(f'zic -d "{zoneinfo_dir}" {extract_dir}/africa {extract_dir}/antarctica '
            #             f'{extract_dir}/asia {extract_dir}/australasia {extract_dir}/etcetera '
            #             f'{extract_dir}/europe {extract_dir}/northamerica {extract_dir}/southamerica')
            tz_files[version] = extract_dir

        return tz_files, tz_dir

    @staticmethod
    def delete_tz_files(folder):
        """Delete the tz_versions folder and all its contents"""
        import shutil
        shutil.rmtree(folder)

    def correct_time_version(self, time_data, time_zone, version):
        shifted_set = set()

        # Inject version-specific tzdata into zoneinfo
        version_dir = self.tz_files[version]
        zoneinfo.ZoneInfo.clear_cache()
        # print(zoneinfo.TZPATH)
        zoneinfo.reset_tzpath([version_dir])
        # print(zoneinfo.TZPATH)

        # Parse timestamp and apply the given time zone from zoneinfo
        timestamp = datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")
        tz_local = zoneinfo.ZoneInfo(time_zone)

        # Convert to aware datetime using zoneinfo
        local_dt = timestamp.replace(tzinfo=tz_local)
        dt_og = local_dt.astimezone(timezone.utc)

        # Recreate the datetime again for comparison
        dt_new = timestamp.replace(tzinfo=tz_local)
        dt_new_utc = dt_new.astimezone(timezone.utc)

        # Check if UTC conversion has changed
        if dt_og != dt_new_utc:
            shifted_set.add(version)

        # Format to ISO 8601 with colon in offset
        dt_fmt = dt_og.strftime('%Y-%m-%dT%H:%M:%S%z')
        dt_fmt = f"{dt_fmt[:-2]}:{dt_fmt[-2:]}"  # insert colon in UTC offset

        print(f"Version: {version}, Local= {dt_new} | UTC= {dt_fmt}")
        return dt_fmt

    def identify_signal_time(self, signal_log, debug: bool = False):
        signal_list = [tuple(line.split('; ')) for line in signal_log]

        self.station_log = defaultdict(int)
        self.research_stations = set()
        self.tz_files, self.tz_dir = self.get_tz_files(self.TZ_VERSIONS)
        sorted_list = []
            # print(version, self.tz_files[version])
        for time_data, zone_str in signal_list[:]:
            if zone_str != 'Antarctica/Casey':
                continue
            print(f"{time_data}; {zone_str}")
            for version in self.TZ_VERSIONS[:]:

                corrected = self.correct_time_version(time_data, zone_str, version)
                self.station_log[corrected] += 1
        total_stations = len(self.research_stations)

        # for stamp, count in self.station_log.items():
        #     print(stamp, count)
        #     if count == total_stations:
        #         print(stamp, "Valid")

        # self.delete_tz_files(self.tz_dir)

        return len(signal_log)

signal_timestamp = TimeLogger().identify_signal_time(input_data, True)
print("UTC Signal Timestamp:", signal_timestamp)


print(f"Execution Time = {time.time() - start_time:.5f}s")

# 2024-04-09T17:49:00+00:00; Antarctica/Casey
# 2024-04-12T14:54:00+00:00; Antarctica/Casey
# 2024-04-12T20:43:00+00:00; Antarctica/Casey

# 2024-04-09T17:19:00+00:00; Asia/Pyongyang
# 2024-04-09T18:49:00+00:00; Africa/Casablanca
# 2024-04-12T03:13:00+00:00; Asia/Pyongyang
# 2024-04-12T15:24:00+00:00; Asia/Pyongyang
# 2024-04-12T15:54:00+00:00; Africa/Casablanca
# 2024-04-12T16:43:00+00:00; Africa/Casablanca

# Consider the following dataset, which serves as your test input:
# 2024-04-09 18:49:00; Africa/Casablanca
# 2024-04-10 02:19:00; Asia/Pyongyang
# 2024-04-10 04:49:00; Antarctica/Casey
# 2024-04-12 12:13:00; Asia/Pyongyang
# 2024-04-12 15:54:00; Africa/Casablanca
# 2024-04-12 16:43:00; Africa/Casablanca
# 2024-04-13 00:24:00; Asia/Pyongyang
# 2024-04-13 01:54:00; Antarctica/Casey
# 2024-04-13 07:43:00; Antarctica/Casey

# These are local times, combined with an IANA time zone identifier,
# for that research station. You convert all of these to UTC, and sort them:
# 2024-04-09T17:19:00+00:00; Asia/Pyongyang
# 2024-04-09T17:49:00+00:00; Antarctica/Casey
# 2024-04-09T18:49:00+00:00; Africa/Casablanca
# 2024-04-12T03:13:00+00:00; Asia/Pyongyang
# 2024-04-12T14:54:00+00:00; Antarctica/Casey
# 2024-04-12T15:24:00+00:00; Asia/Pyongyang
# 2024-04-12T15:54:00+00:00; Africa/Casablanca
# 2024-04-12T16:43:00+00:00; Africa/Casablanca
# 2024-04-12T20:43:00+00:00; Antarctica/Casey

# 2024-04-09 18:49:00; Africa/Casablanca converts to 2024-04-09T17:49:00+00:00.
# 2024-04-10 02:19:00; Asia/Pyongyang converts to 2024-04-09T17:49:00+00:00.
# 2024-04-10 04:49:00; Antarctica/Casey converts to 2024-04-09T17:49:00+00:00.
# 2024-04-12 12:13:00; Asia/Pyongyang converts to 2024-04-12T03:43:00+00:00.
# 2024-04-12 15:54:00; Africa/Casablanca converts to 2024-04-12T14:54:00+00:00.
# 2024-04-12 16:43:00; Africa/Casablanca converts to 2024-04-12T15:43:00+00:00.
# 2024-04-13 00:24:00; Asia/Pyongyang converts to 2024-04-12T15:54:00+00:00.
# 2024-04-13 01:54:00; Antarctica/Casey converts to 2024-04-12T14:54:00+00:00.
# 2024-04-13 07:43:00; Antarctica/Casey converts to 2024-04-12T20:43:00+00:00.