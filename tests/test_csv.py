import csv

import pytest

from streamstats import parser
from streamstats.errors import StreamStatsError


def test_parser_csv(tmp_path):
    expected = {
        "timestamp": "2026-07-19T22:38:13",
        "level": "CRITICAL",
        "source": "linux",
        "message": "критическая ошибка"
    }

    stats = {"skipped_lines": 0}

    path = tmp_path / "valid.csv"

    with path.open("w", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "level", "source", "message"],
        )
        writer.writeheader()
        writer.writerow(expected)

    with path.open("r", encoding="utf-8") as file:
        result = list(parser.parser_csv(stats, file))

    assert stats["skipped_lines"] == 0
    assert result == [expected]

def test_parser_csv_error(tmp_path):
    expected = {
        "timestamp": "2026-07-19T22:38:13",
        "level": "CRITICAL",
        "source": "",
        "message": "критическая ошибка"
    }

    stats = {"skipped_lines": 0}
    path = tmp_path / "invalid.csv"

    with path.open("w", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "level", "source", "message"],
        )
        writer.writeheader()
        writer.writerow(expected)

    with path.open("r", encoding="utf-8") as file, pytest.raises(StreamStatsError):
        list(parser.parser_csv(stats, file))

    with path.open("r", encoding="utf-8") as file:
        list(parser.parser_csv(stats, file, skip_invalid=True))

    assert stats["skipped_lines"] == 1

def test_empty_file_parser_csv(tmp_path):
    path = tmp_path / "empty.csv"
    path.touch()
    stats = {"skipped_lines": 0}

    with path.open("r", encoding="utf-8") as file:
        result = list(parser.parser_csv(stats, file))

    assert result == []
    assert stats["skipped_lines"] == 0

