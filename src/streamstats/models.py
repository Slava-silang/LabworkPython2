from datetime import datetime

from .errors import StreamStatsParseError, StreamStatsTimestampError

ALLOWED_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def validate_line(line: dict, file: str, line_number: int) -> None:
    """The function for checking if a line is valid"""

    root_error = f"ERROR: file {file} line {line_number}" # sample for errors

    if line.get('timestamp') is None: # Checking necessary fields
        raise StreamStatsParseError(f"{root_error}: timestamp field is required")

    if line.get("level") is None:
        raise StreamStatsParseError(f"{root_error}: level field is required")

    if line.get("source") is None:
        raise StreamStatsParseError(f"{root_error}: source field is required")

    timestamp = line["timestamp"] # Getting fields
    level = line["level"]
    source = line["source"]

    if level not in ALLOWED_LEVELS: # Check whether level is allowed
        raise StreamStatsParseError(f"{root_error}: level field must be one of {ALLOWED_LEVELS}")

    if source == "": # Check whether source is empty
        raise StreamStatsParseError(f"{root_error}: source field cannot be empty")

    try: # Trying to make time from ISO format and raise exception if it is not
        datetime.fromisoformat(timestamp)
    except ValueError:
        raise StreamStatsTimestampError(f"{root_error}: timestamp field must be ISO8601 format")
