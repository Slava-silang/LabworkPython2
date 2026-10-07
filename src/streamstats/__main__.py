import argparse

from . import analysis
from . import report


def main():
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
        help='Input format (default: jsonl)'
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

    rep = analysis.analyze(args.INPUT, args.format, args.skip_invalid)
    report.write_report(rep, args.output)


if __name__ == '__main__':
    main()
