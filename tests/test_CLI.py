import csv
import json
import subprocess
import sys

data_one = [
        {"timestamp": "2024-11-09T20:43:02", "level": "ERROR", "source": "api", "message": ""},
        {"timestamp": "2021-01-23T11:55:25", "level": "ERROR", "source": "yandex", "message": ""},
        {"timestamp": "2020-01-22T14:23:39", "level": "CRITICAL", "source": "program", "message": ""},
        {"timestamp": "2021-05-19T14:01:00", "level": "ERROR", "source": "api", "message": ""},
    ]
data_two = [
        {"timestamp": "2020-04-16T13:39:20", "level": "ERROR", "source": "linux", "message": ""},
        {"timestamp": "2020-04-04T11:34:32", "level": "INFO", "source": "app", "message": ""},
        {"timestamp": "2021-01-08T13:24:42", "level": "DEBUG", "source": "yandex", "message": ""},
        {"timestamp": "2024-09-29T11:35:36", "level": "ERROR", "source": "linux", "message": ""},
        ]
data_three = [
        {"timestamp": "2025-12-06T23:58:50", "level": "INFO", "source": "program", "message": ""},
        {"timestamp": "2021-11-17T10:43:25", "level": "WARNING", "source": "program", "message": ""},
        {"timestamp": "2021-07-02T05:49:54", "level": "WARNING", "source": "api", "message": ""},
        {"timestamp": "2022-05-21T16:20:28", "level": "CRITICAL", "source": "lala", "message": ""},
        ]

expected = {
        "min_timestamp": "2020-01-22T14:23:39+00:00",
        "max_timestamp": "2025-12-06T23:58:50+00:00",
        "total_events": 12,
        "level": {
            "ERROR": 5,
            "CRITICAL": 2,
            "INFO": 2,
            "DEBUG": 1,
            "WARNING": 2,
        },
        "source": {
            "api": 3,
            "yandex": 2,
            "program": 3,
            "linux": 2,
            "app": 1,
            "lala": 1
        },
        "top_ERROR|CRITICAL_sources": [
            {
                "sources": "api",
                "count": 2
            },
            {
                "sources": "linux",
                "count": 2
            },
            {
                "sources": "lala",
                "count": 1
            },
            {
                "sources": "program",
                "count": 1
            },
            {
                "sources": "yandex",
                "count": 1
            }
        ]
}

def test_cli_jsonl(tmp_path) -> None:

    first_file = tmp_path / "first_file.jsonl"
    second_file = tmp_path / "second_file.jsonl"
    third_file = tmp_path / "third_file.jsonl"

    for file in [[first_file, data_one], [second_file, data_two], [third_file, data_three]]:
        file_path = file[0]
        data = file[1]
        with file_path.open("w", encoding="utf-8") as f:
            for line in data:
                json.dump(line, f, ensure_ascii=False)
                f.write("\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            "--format",
            "jsonl",
            str(first_file),
            str(second_file),
            str(third_file),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report == expected

def test_cli_csv(tmp_path):
    first_file = tmp_path / "first_file.csv"
    second_file = tmp_path / "second_file.csv"
    third_file = tmp_path / "third_file.csv"

    for file in [[first_file, data_one], [second_file, data_two], [third_file, data_three]]:
        file_path = file[0]
        data = file[1]
        with file_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["timestamp", "level", "source", "message"]
            )
            writer.writeheader()
            for line in data:
                writer.writerow(line)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            "--format",
            "csv",
            str(first_file),
            str(second_file),
            str(third_file),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report == expected
