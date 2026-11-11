import argparse
from collections import Counter
from pathlib import Path
from pprint import pprint
from time import perf_counter

from app.parser import parse_line


def inspect_logs(path):
    levels = Counter()
    parsed_count = 0
    failed_count = 0
    start = perf_counter()

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                event = parse_line(line)
            except ValueError as error:
                failed_count += 1

                if failed_count <= 5:
                    print(f"Line {line_number}: {error}")

                continue

            parsed_count += 1
            levels[event["level"]] += 1

            if parsed_count == 1:
                print("First parsed event:")
                pprint(event)

            if parsed_count % 100_000 == 0:
                print(f"Parsed {parsed_count:,} lines", flush=True)

    elapsed = perf_counter() - start

    print()
    print(f"Parsed lines: {parsed_count:,}")
    print(f"Failed lines: {failed_count:,}")
    print(f"Log levels: {dict(levels)}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"Parsing speed: {parsed_count / elapsed:,.0f} lines/second")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect an HDFS log file")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    inspect_logs(args.path)