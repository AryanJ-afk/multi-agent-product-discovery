from pathlib import Path

from app.db import get_connection
from app.parser import parse_line


def ingest_logs(path):
    schema_path = Path(__file__).with_name("schema.sql")
    source_file = path.name
    count = 0

    with get_connection() as connection:
        connection.execute(schema_path.read_text(encoding="utf-8"))

        existing = connection.execute(
            "SELECT 1 FROM log_events WHERE source_file = %s LIMIT 1",
            (source_file,),
        ).fetchone()

        if existing:
            print(f"{source_file} is already imported. Skipping.")
            return

        with connection.cursor() as cursor:
            with cursor.copy("""
                COPY log_events (
                    source_file,
                    line_number,
                    timestamp,
                    thread_id,
                    level,
                    component,
                    message,
                    block_ids
                )
                FROM STDIN
            """) as copy:
                with path.open(encoding="utf-8") as file:
                    for line_number, line in enumerate(file, start=1):
                        try:
                            event = parse_line(line)
                        except ValueError as error:
                            raise ValueError(
                                f"{source_file}, line {line_number}: {error}"
                            ) from error

                        copy.write_row((
                            source_file,
                            line_number,
                            event["timestamp"],
                            event["thread_id"],
                            event["level"],
                            event["component"],
                            event["message"],
                            event["block_ids"],
                        ))

                        count += 1

    print(f"Imported {count} events from {source_file}")


if __name__ == "__main__":
    ingest_logs(Path("data/raw/HDFS_2k.log"))