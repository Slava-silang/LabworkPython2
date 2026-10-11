import csv
import json
import logging
from collections.abc import Generator
from json import JSONDecodeError

from .errors import StreamStatsError
from .models import validate_line

logger = logging.getLogger(__name__) # Loading warning logger


def parser_jsonl(stats: dict, file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    """The function to validate and yield line from jsonl file."""
    for line_number, line in enumerate(file, start=1): # Get line from file
        try:
            data = json.loads(line)  # Reform it with json
            validate_line(data, file, line_number) # Validate line
        except StreamStatsError as error:
            if skip_invalid: # Check mode
                logger.warning( # Makes warning if mode is skip invalid
                    "Skipping invalid line %s: %s. %s",
                    line_number,
                     line,
                     error
                )
                stats['skipped_lines'] += 1 # Add one to skip lines
                continue

            raise # Raise error if mode is not skip invalid
        except JSONDecodeError as error:
            if skip_invalid:
                logger.warning(
                    "Skipping invalid line %s: %s. %s",
                    line_number,
                    line,
                    error
                )
                stats['skipped_lines'] += 1
                continue

            raise StreamStatsError(f'Invalid line {line_number}: {line}')

        yield data # Return data line by line to avoid memory overflow

def parser_csv(stats: dict, file, skip_invalid: bool = False) -> Generator[dict, None, None]:
    """The function to validate and yield line from csv file."""
    reader = csv.DictReader(file) # Make csv dict reader
    count_line = 1
    for row in reader: # Sort through lines
        count_line += 1
        try: # Trying to validate line
            validate_line(row, file, count_line)
        except StreamStatsError as error:
            if skip_invalid: # Check mode
                logger.warning( # Make warning if mode is skip invalid
                    "Skipping invalid line %s: %s. %s",
                    count_line,
                    row,
                    error
                )
                stats['skipped_lines'] += 1 # Add one to skipped lines counter
                continue

            raise # Raise error if mode is not skip invalid

        yield row # Return data line by line to avoid memory overflow
