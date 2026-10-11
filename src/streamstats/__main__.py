import argparse
import logging
import sys
from json import JSONDecodeError
from pathlib import Path

from streamstats.errors import StreamStatsError

from . import analysis, report


def main() -> int:
    """Main entry point
    Translate arguments from command line and run"""
    logging.basicConfig(                                # Initialisation warnings
        level=logging.WARNING,
        format='%(levelname)s %(asctime)s %(message)s', # Format for output warnings
        filename='WARNING.log',                         # Output file for warnings
        encoding='utf-8',                               # For russian lines
    )
    parser = argparse.ArgumentParser()                  # Initialisation parser
    parser.add_argument(                                # First argument
        'command',
        choices=['analyze'],
        type=str,
        help='Command to run'
    )
    parser.add_argument(                                # Second argument
        'INPUT',
        type=str,
        nargs='+',
        help='Input files'
    )
    parser.add_argument(                                # Format argument
        '--format',
        type=str,
        default='jsonl',
        help='Input format',
        choices=['jsonl', 'csv'],
        required=True
    )
    parser.add_argument(                                # Output argument
        '--output',
        type=str,
        default='-',                                    # If user did not write output file
        help='Output file (default: stdout)'            # program writes report to stdout
    )
    parser.add_argument(                                # Skip invalid argument
        '--skip-invalid',
        action='store_true',
        help='Skip invalid records'
    )
    args = parser.parse_args()
    try:
        path_output = Path(args.output).resolve()
        for input_file in args.INPUT:
            if path_output == Path(input_file).resolve():
                raise StreamStatsError(f"{input_file} already contains information")
        stats, error_critical = analysis.analyze(args.INPUT, args.format, args.skip_invalid)
        report.write_report(stats, error_critical, args.output)
        # Writes report if program has success
    except StreamStatsError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2
    except FileNotFoundError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2
    except JSONDecodeError as error:
        print(f'ERROR: {error}', file=sys.stderr)
    # Raises error if program meets invalid line without --skip-invalid
    return 0


if __name__ == '__main__':
    raise SystemExit(main()) # To indicate system exit
