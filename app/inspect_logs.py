from collections import Counter
from pathlib import Path
from pprint import pprint

from app.parser import parse_line


def inspect_logs(path):
    levels = Counter()
    parsed_count = 0
    failed_count = 0

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                event = parse_line(line)
            except ValueError as error:
                failed_count += 1
                print(f"Line {line_number}: {error}")
                continue

            parsed_count += 1
            levels[event["level"]] += 1

            if parsed_count == 1:
                print("First parsed event:")
                pprint(event)

    print()
    print(f"Parsed lines: {parsed_count}")
    print(f"Failed lines: {failed_count}")
    print(f"Log levels: {dict(levels)}")


if __name__ == "__main__":
    inspect_logs(Path("data/raw/HDFS_2k.log"))