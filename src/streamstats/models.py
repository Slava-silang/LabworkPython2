from datetime import datetime

from .errors import StreamStatsParseError, StreamStatsTimestampError

ALLOWED_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def validate_line(line: dict, file: str, line_number: int) -> None:

    root_error = f"ERROR: file {file} line {line_number}"

    if line.get('timestamp') is None:
        raise StreamStatsParseError(f"{root_error}: timestamp field is required")

    if line.get("level") is None:
        raise StreamStatsParseError(f"{root_error}: level field is required")

    if line.get("source") is None:
        raise StreamStatsParseError(f"{root_error}: source field is required")

    timestamp = line["timestamp"]
    level = line["level"]
    source = line["source"]

    if level not in ALLOWED_LEVELS:
        raise StreamStatsParseError(f"{root_error}: level field must be one of {ALLOWED_LEVELS}")

    if source == "":
        raise StreamStatsParseError(f"{root_error}: source field cannot be empty")

    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        raise StreamStatsTimestampError(f"{root_error}: timestamp field must be ISO8601 format")
