from datetime import UTC, datetime

from .errors import UnsupportedTypeOfFileError
from .parser import parser_csv, parser_jsonl


def analyze(input_files: list[str], input_format: str, skip_invalid:bool=False):
    max_time: datetime | None = None
    min_time: datetime | None = None
    stats = {
        "min_time": "",
        "max_time": "",
        "total_events": 0,
        "level": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "source": {},
    }
    if skip_invalid:
        stats["skipped_lines"] = 0
    error_critical = {}
    for path in input_files:

        if path.endswith(".jsonl") == path.endswith(".csv") == False:
            raise UnsupportedTypeOfFileError(f"File {path} does not end with .jsonl or .csv")

        with open(path, 'r', encoding='utf8', newline="") as file:
            if input_format == "jsonl":
                events = parser_jsonl(stats, file, skip_invalid)

            else:
                events = parser_csv(stats, file, skip_invalid)

            for event in events:
                level = event["level"]
                source = event["source"]

                stats["level"][level] += 1
                stats["total_events"] += 1

                if level in ["ERROR", "CRITICAL"]:

                    if source not in error_critical:
                        error_critical[source] = 0

                    error_critical[source] += 1

                if source not in stats["source"]:
                    stats["source"][source] = 0

                stats["source"][source] += 1

                time = datetime.fromisoformat(event["timestamp"])
                if time.tzinfo is None:
                    time = time.replace(tzinfo=UTC)

                if max_time is None or time > max_time:
                    max_time = time

                if min_time is None or time < min_time:
                    min_time = time

    stats["max_time"] = max_time
    stats["min_time"] = min_time

    return stats, error_critical