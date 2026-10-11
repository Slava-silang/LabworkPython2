from datetime import UTC, datetime

from .errors import UnsupportedTypeOfFileError
from .parser import parser_csv, parser_jsonl


def analyze(input_files: list[str], input_format: str, skip_invalid:bool=False) -> tuple[dict, dict]:
    """The analysis function counts data and return dicts with information"""
    max_time: datetime | None = None # Initialisation for max time
    min_time: datetime | None = None # Initialisation for min time
    stats = {                        # The data for report
        "min_timestamp": "",
        "max_timestamp": "",
        "total_events": 0,
        "level": {},
        "source": {},
    }
    if skip_invalid:
        stats["skipped_lines"] = 0   # Adds paragraph for counting skipped lines
    error_critical = {}              # If program in skip-invalid mode
    for path in input_files:
        # Additional compliance check file
        if path.endswith(".jsonl") == path.endswith(".csv") == False:
            raise UnsupportedTypeOfFileError(f"File {path} does not end with .jsonl or .csv")
        if path.endswith(".jsonl") and input_format == "csv":
            raise UnsupportedTypeOfFileError(f"File {path} cannot be opened with csv module")
        if path.endswith(".csv") and input_format == "jsonl":
            raise UnsupportedTypeOfFileError(f"File {path} cannot be opened with json module")

        with open(path, 'r', encoding='utf8', newline="") as file: # Starting to sort through files
            if input_format == "jsonl": # Check input format
                events = parser_jsonl(stats, file, skip_invalid) # Get lines from jsonl file

            else:
                events = parser_csv(stats, file, skip_invalid)   # Get lines from csv file

            for event in events:                                 # Sort through lines
                level = event["level"]                           # Get necessary fields
                source = event["source"]

                if level not in stats["level"]:                  # Init fields if they have not
                    stats["level"][level] = 0

                stats["level"][level] += 1                       # Add one to gotten field

                stats["total_events"] += 1

                if level in ["ERROR", "CRITICAL"]:

                    if source not in error_critical:
                        error_critical[source] = 0

                    error_critical[source] += 1                  # Counting error critical sources

                if source not in stats["source"]:
                    stats["source"][source] = 0                  # Counting sources

                stats["source"][source] += 1

                time = datetime.fromisoformat(event["timestamp"])# Reform time
                if time.tzinfo is None:
                    time = time.replace(tzinfo=UTC)              # Makes UTS time

                if max_time is None or time > max_time:          # Comparing and updating time fields
                    max_time = time

                if min_time is None or time < min_time:
                    min_time = time

    stats["max_timestamp"] = max_time.isoformat() if max_time is not None else "" # Change parameters
    stats["min_timestamp"] = min_time.isoformat() if min_time is not None else ""

    return stats, error_critical # Return main statistic and error critical sources count
