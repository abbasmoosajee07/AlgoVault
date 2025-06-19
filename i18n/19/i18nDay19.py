"""i18n Puzzles - Puzzle 19
Solution Started: Jun 11, 2025
Puzzle Link: https://i18n-puzzles.com/puzzle/19
Solution by: Abbas Moosajee
Brief: [Out of date]
"""

#!/usr/bin/env python3

from pathlib import Path
import os, re, copy, time
import requests, tarfile, shutil
from collections import defaultdict
from datetime import timezone, datetime
from zoneinfo import reset_tzpath, ZoneInfo
start_time = time.time()

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n')

class TimeLogger:
    TZ_VERSIONS = ('2018c', '2018g', '2021b', '2023d')

    def __init__(self, cleanup: bool = True, debug: bool = False):
        self.cleanup, self.debug = (cleanup, debug)
        self.base_dir = Path(__file__).resolve().parent / "old_tzdata"
        self.extract_dir = self.base_dir / "extracted"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.extract_dir.mkdir(parents=True, exist_ok=True)
        self.tz_files = self.get_tz_files(self.TZ_VERSIONS)

    @staticmethod
    def get_package_and_version(version_name: str) -> tuple[str, str]:
        """Map a tz version to the appropriate package and dotted version format."""
        def conv_version(name: str) -> str:
            return f"{name[:-1]}.{ord(name[-1]) - ord('a') + 1}"

        if version_name < "2013f":
            return "pytz", version_name
        elif version_name < "2016g":
            return "pytz", conv_version(version_name)
        elif version_name < "2020a":
            return "pytzdata", conv_version(version_name)
        return "tzdata", conv_version(version_name)

    def download_tarball(self, package: str, version: str) -> Path:
        """Download tzdata tarball if not already present."""
        tarball_path = self.base_dir / f"{package}-{version}.tar.gz"
        if tarball_path.exists():
            return tarball_path

        url = f"https://files.pythonhosted.org/packages/source/{package[0]}/{package}/{package}-{version}.tar.gz"
        if self.debug:
            print(f"⬇️ Downloading {package}-{version} from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with tarball_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return tarball_path

    @staticmethod
    def find_and_copy_zoneinfo(root_dir: Path, output_dir: Path, version: str) -> Path:
        """Locate and copy the 'zoneinfo' folder from an extracted tree."""
        for dirpath, _, _ in os.walk(root_dir):
            if Path(dirpath).name == "zoneinfo":
                dest = output_dir / f"{version}_zoneinfo"
                shutil.copytree(dirpath, dest, dirs_exist_ok=True)
                return dest
        raise FileNotFoundError(f"No 'zoneinfo' folder found in {root_dir}.")

    def extract_zoneinfo(self, tarball_path: Path, package: str, version_name: str) -> Path:
        """Extract tarball and find 'zoneinfo'."""
        extract_path = self.extract_dir / f"{package}-{version_name}"
        if not extract_path.exists() or not any(extract_path.iterdir()):
            with tarfile.open(tarball_path, "r:gz") as tar:
                tar.extractall(path=extract_path, filter="tar")
        return self.find_and_copy_zoneinfo(extract_path, self.extract_dir, version_name)

    def get_tz_files(self, required_tz: list[str]) -> dict[str, str]:
        """Download and extract required tzdata files."""
        tz_files = {}
        for version_name in required_tz:
            package, version = self.get_package_and_version(version_name)
            tarball = self.download_tarball(package, version)
            zoneinfo_path = self.extract_zoneinfo(tarball, package, version_name)
            tz_files[version_name] = str(zoneinfo_path)
            if self.debug:
                print(f"Version {version_name} saved to {str(zoneinfo_path)}")
        return tz_files

    @staticmethod
    def delete_tz_files(folder: Path):
        """Delete the extracted tz folder."""
        shutil.rmtree(folder, ignore_errors=True)

    def parse_signal_log(self, signal_log: list[str]) -> dict[str, list[datetime]]:
        """Parse signal log entries into a dict of time zone → list of timestamps."""
        parsed = defaultdict(list)
        for line in signal_log:
            time_str, zone_str = line.split('; ')
            timestamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            parsed[zone_str].append(timestamp)
        return parsed

    @staticmethod
    def convert_to_utc(timestamp: datetime, zone_str: str) -> datetime:
        """Convert local timestamp in a time zone to UTC."""
        tz_local = ZoneInfo(zone_str)
        dt_local = timestamp.replace(tzinfo=tz_local)
        dt_utc = dt_local.astimezone(timezone.utc)
        return dt_utc

    def identify_signal_time(self, signal_log: list[str]) -> str | None:
        """Determine the UTC time at which all zones agree on the signal."""
        signal_dict = self.parse_signal_log(signal_log)
        station_log = defaultdict(set)
        identified_signal = None
        debug_list = []

        for version, zoneinfo_path in self.tz_files.items():
            reset_tzpath([zoneinfo_path])
            ZoneInfo.clear_cache()
            for zone, times in signal_dict.items():
                for timestamp in times:
                    corrected = self.convert_to_utc(timestamp, zone)
                    station_log[corrected].add(zone)
                    debug_list.append((version, zone, timestamp, corrected))

        for stamp, zones in station_log.items():
            if self.debug:
                print(f"UTC: {stamp} |{len(zones)} Zones {zones}")
            if len(zones) == len(signal_dict):
                dt_str = stamp.strftime('%Y-%m-%dT%H:%M:%S%z')
                if self.cleanup:
                    self.delete_tz_files(self.extract_dir)
                identified_signal = f"{dt_str[:-2]}:{dt_str[-2:]}"
                if not self.debug:
                    break
        return identified_signal

signal_timestamp = TimeLogger().identify_signal_time(input_data)
print("Signal Timestamp UTC:", signal_timestamp)

print(f"Execution Time = {time.time() - start_time:.5f}s")
