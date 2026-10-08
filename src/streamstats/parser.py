import csv
import json
from collections.abc import Generator
from .models import validate_line


def parser_jsonl(file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    for line_number, line in enumerate(file, start=1):
        data = json.loads(line)
        yield data

def parser_csv(file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    reader = csv.DictReader(file)
    for row in reader:
        event = validate_line(row)

        yield row
