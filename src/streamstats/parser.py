import csv
import json
import logging
from collections.abc import Generator

from .errors import StreamStatsError
from .models import validate_line

logger = logging.getLogger(__name__)


def parser_jsonl(stats: dict, file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    for line_number, line in enumerate(file, start=1):
        data = json.loads(line)
        try:
            validate_line(data)
        except StreamStatsError as error:
            if skip_invalid:
                logger.warning(f"Skipping invalid line {line_number}: {line}", error)
                stats['skipped_lines'] += 1
                continue

            raise

        yield data

def parser_csv(stats: dict, file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    reader = csv.DictReader(file)
    count_line = 0
    for row in reader:
        count_line += 1
        try:
            validate_line(row)
        except StreamStatsError as error:
            if skip_invalid:
                logger.warning(f"Skipping invalid line {count_line}: {row}", error)
                stats['skipped_lines'] += 1
                continue

            raise

        yield row
