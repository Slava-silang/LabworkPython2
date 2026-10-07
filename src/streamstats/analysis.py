from .errors import StreamStatsError
from .parser import parse_csv, parse_jsonl


def analyze(input_files: list[str], input_format: str, skip_invalid:bool=False) -> dict:
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
        "ERROR|CRITICAL": {}
    }
    for path in input_files:

        with open(path, 'r', encoding='utf8', newline="") as file:
            if input_format == "jsonl":
                events = parse_jsonl(file, skip_invalid)

            elif input_format == "csv":
                events = parse_csv(file, skip_invalid)

            else:
                raise StreamStatsError(f"Unsupported input format: {input_format}")

            for event in events:
                level = event.get("level")
                source = event.get("source")

                stats["level"][level] += 1
                stats["total_events"] += 1

                if level in ["ERROR", "CRITICAL"]:

                    if source not in stats["ERROR|CRITICAL"]:
                        stats["ERROR|CRITICAL"][source] = 0

                    stats["ERROR|CRITICAL"][source] += 1

                if source not in stats["source"]:
                    stats["source"][source] = 0

                stats["source"][source] += 1

    return stats