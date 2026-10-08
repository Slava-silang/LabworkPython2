import argparse
import logging
import sys

from streamstats.errors import StreamStatsError, UnsupportedTypeOfFileError

from . import analysis, report


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(levelname)s %(asctime)s %(message)s',
        filename='WARNING.log',
        encoding='utf-8',
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',
        choices=['analyze'],
        type=str,
        help='Command to run'
    )
    parser.add_argument(
        'INPUT',
        type=str,
        nargs='+',
        help='Input files'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='jsonl',
        help='Input format',
        choices=['jsonl', 'csv'],
        required=True
    )
    parser.add_argument(
        '--output',
        type=str,
        default='-',
        help='Output file (default: stdout)'
    )
    parser.add_argument(
        '--skip-invalid',
        action='store_true',
        help='Skip invalid records'
    )
    args = parser.parse_args()
    try:
        stats, error_critical = analysis.analyze(args.INPUT, args.format, args.skip_invalid)
        report.write_report(stats, error_critical, args.output)
    except UnsupportedTypeOfFileError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2
    except StreamStatsError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2
    except FileNotFoundError as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
