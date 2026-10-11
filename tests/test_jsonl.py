import json

import pytest

from streamstats import parser
from streamstats.errors import StreamStatsError


def test_jsonl_parser(tmp_path):
    expected = [
        {
            "timestamp": "2025-08-22T20:26:36",
            "level": "WARNING",
            "source": "yandex",
            "message": "соединение прервано",
        },
        {
            "timestamp": "2025-04-21T14:57:14",
            "level": "ERROR",
            "source": "yandex",
            "message": "сайт не найден",
        }
    ]
    path = tmp_path / "valid.jsonl"

    with path.open("w", encoding="utf-8") as file:
        for line in expected:
            json.dump(line, file, ensure_ascii=False)
            file.write("\n")

    with path.open(encoding="utf-8") as file:
        result = list(parser.parser_jsonl({"skipped_lines": 0}, file))

    assert result == expected

def test_invalid_jsonl_parser(tmp_path):
    path = tmp_path / "invalid.jsonl"

    expected = {
        "timestamp": "2026-07-19T22:38:13",
        "level": "CRITICAL",
        "source": "",
        "message": "критическая ошибка"
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(expected, file, ensure_ascii=False)
        file.write("\n")

    stats = {"skipped_lines": 0}

    with path.open(encoding="utf-8") as file, pytest.raises(StreamStatsError):
        list(parser.parser_jsonl(stats, file))

    with path.open(encoding="utf-8") as file:
        list(parser.parser_jsonl(stats, file, skip_invalid=True))
        assert stats["skipped_lines"] == 1

def test_empty_file_jsonl_parser(tmp_path):
    path = tmp_path / "empty.jsonl"

    path.touch()

    with path.open(encoding="utf-8") as file:
        result = list(parser.parser_jsonl({"skipped_lines": 0}, file))
        assert result == []