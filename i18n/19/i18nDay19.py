# %%
"""i18n Puzzles - Puzzle 19
Solution Started: Jun 11, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/19
Solution by: Abbas Moosajee
Brief: [Out of date]
"""

#!/usr/bin/env python3

import os, re, copy, time
from collections import defaultdict
from zoneinfo import reset_tzpath, ZoneInfo
from datetime import timezone, datetime
import requests, os, time, tarfile, shutil
start_time = time.time()

# Load the input data from the specified file path
D19_file = "Day19_input1.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n')

class TimeLogger:
    TZ_VERSIONS = ('2018c', '2018g', '2021b', '2023d')
    LOG_FORMAT  = '%Y-%m-%dT%H:%M:%S%z'

    @staticmethod
    def get_package_and_version(version_name: str) -> tuple[str, str]:
        """Decide which package to use and convert version if needed."""
        def conv_version(tz_version: str) -> str:
            """Convert from lettered tzdata version (e.g., '2018c') to dotted format (e.g., '2018.3')"""
            num_version = ord(tz_version[-1]) - ord('a') + 1
            return f"{tz_version[:-1]}.{num_version}"

        if version_name < "2013f":
            return "pytz", version_name
        elif version_name < "2016g":
            return "pytz", conv_version(version_name)
        elif version_name < "2020a":
            return "pytzdata", conv_version(version_name)
        else:
            return "tzdata", conv_version(version_name)

    @staticmethod
    def find_and_copy_zoneinfo(root_dir: str, output_dir: str, version: str) -> str:
        for dirpath, _, _ in os.walk(root_dir):
            if os.path.basename(dirpath) == "zoneinfo":
                dest = os.path.join(output_dir, f"{version}_zoneinfo")
                shutil.copytree(dirpath, dest, dirs_exist_ok=True)
                return dest
        raise FileNotFoundError("No 'zoneinfo' folder found in the given directory.")

    @staticmethod
    def download_tarball(package: str, version: str, base_dir: str) -> str:
        """Download the tarball file from PyPI if it doesn't already exist."""
        tarball_path = os.path.join(base_dir, f"{package}-{version}.tar.gz")
        if os.path.exists(tarball_path):
            return tarball_path

        url = f"https://files.pythonhosted.org/packages/source/{package[0]}/{package}/{package}-{version}.tar.gz"
        print(f"⬇️ Downloading {package}-{version} from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(base_dir, exist_ok=True)
        with open(tarball_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return tarball_path

    def extract_tarball_and_find_zoneinfo(self, tarball_path: str, extract_base: str, package: str, version_name: str) -> str:
        """Extract the tarball if needed and return the path to the copied zoneinfo folder."""
        extract_dir = os.path.join(extract_base, f"{package}-{version_name}")
        os.makedirs(extract_base, exist_ok=True)

        if not os.path.exists(extract_dir) or not os.listdir(extract_dir):
            with tarfile.open(tarball_path, "r:gz") as tar:
                tar.extractall(path=extract_dir, filter="tar")

        return self.find_and_copy_zoneinfo(extract_dir, extract_base, version_name)

    def get_tz_files(self, required_tz, tz_folder = "old_tzdata"):
        """Download and extract tzdata-<version>.tar.gz files from IANA"""
        tz_files = {}

        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), tz_folder)
        extract_base = os.path.join(base_dir, "extracted")
        for version_name in required_tz:
            package, version = self.get_package_and_version(version_name)
            tarball_path = self.download_tarball(package, version, base_dir)
            path = self.extract_tarball_and_find_zoneinfo(tarball_path, extract_base, package, version_name)
            tz_files[version_name] = path
        return tz_files, extract_base

    @staticmethod
    def delete_tz_files(folder):
        """Delete the extracted folder and all its contents"""
        shutil.rmtree(folder)

    def correct_time_version(self, time_data, time_zone):
        # Parse timestamp and apply the given time zone from zoneinfo
        timestamp = datetime.strptime(time_data, "%Y-%m-%d %H:%M:%S")
        tz_local = ZoneInfo(time_zone)

        # Convert to aware datetime using zoneinfo
        local_dt = timestamp.replace(tzinfo=tz_local)
        dt_og = local_dt.astimezone(timezone.utc)

        # Format to ISO 8601 with colon in offset
        dt_fmt = dt_og.strftime('%Y-%m-%dT%H:%M:%S%z')
        dt_fmt = f"{dt_fmt[:-2]}:{dt_fmt[-2:]}"  # insert colon in UTC offset

        # print(f"Local= {dt_og} | UTC= {dt_fmt}")
        return dt_fmt

    def identify_signal_time(self, signal_log, debug: bool = False):
        self.tz_files, self.tz_dir = self.get_tz_files(self.TZ_VERSIONS)
        signal_list = [tuple(line.split('; ')) for line in signal_log]

        self.station_log = defaultdict(int)
        self.research_stations = set()
        for version in self.TZ_VERSIONS[:]:
            version_dir = self.tz_files[version]
            ZoneInfo.clear_cache()
            reset_tzpath([version_dir])
            for time_data, zone_str in signal_list[:]:
                corrected = self.correct_time_version(time_data, zone_str)
                self.station_log[corrected] += 1

        total_stations = len(self.TZ_VERSIONS)
        for stamp, count in self.station_log.items():
            # print(stamp, count)
            if count == total_stations:
                print(stamp, "Valid")

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