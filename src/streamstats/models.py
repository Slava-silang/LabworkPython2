from datetime import datetime

from .errors import StreamStatsParseError, StreamStatsTimestampError

ALLOWED_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def validate_line(line: dict):

    if line.get('timestamp') is None:
        raise StreamStatsParseError("timestamp field is required")

    if line.get("level") is None:
        raise StreamStatsParseError("level field is required")

    if line.get("source") is None:
        raise StreamStatsParseError("source field is required")

    timestamp = line["timestamp"]
    level = line["level"]
    source = line["source"]

    if level not in ALLOWED_LEVELS:
        raise StreamStatsParseError(f"level field must be one of {ALLOWED_LEVELS}")

    if source == "":
        raise StreamStatsParseError("source field cannot be empty")

    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        raise StreamStatsTimestampError("timestamp field must be ISO8601 format")
