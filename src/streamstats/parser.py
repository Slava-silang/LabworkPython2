import csv
import json
from collections.abc import Generator


def parser_jsonl(file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    """
    Parse a JSONL file and return a list of dictionaries.

    Args:
        file (file object): The input file object.
        skip_invalid (bool): Whether to skip invalid records.

    Yields:
        dict: A dictionary representing a single record from the JSONL file.
    """
    for line_number, line in enumerate(file, start=1):
        data = json.loads(line)
        yield data

def parser_csv(file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    """
    Parse a CSV file and return a list of dictionaries.

    Args:
        file (file object): The input file object.
        skip_invalid (bool): Whether to skip invalid records.

    Yields:
        dict: A dictionary representing a single record from the CSV file.
    """
    reader = csv.DictReader(file)
    for row in reader:
        yield row
