from .errors import StreamStatsError
from .parser import parse_csv, parse_jsonl


def analyze(input_files: list[str], input_format: str, skip_invalid:bool=False):
    stats = {
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
    error_critical = {}
    for path in input_files:

        with open(path, 'r', encoding='utf8', newline="") as file:
            if input_format == "jsonl":
                events = parse_jsonl(file, skip_invalid)

            else:
                events = parse_csv(file, skip_invalid)

            for event in events:
                level = event.get("level")
                source = event.get("source")

                stats["level"][level] += 1
                stats["total_events"] += 1

                if level in ["ERROR", "CRITICAL"]:

                    if source not in error_critical:
                        error_critical[source] = 0

                    error_critical[source] += 1

                if source not in stats["source"]:
                    stats["source"][source] = 0

                stats["source"][source] += 1

    return stats, error_critical