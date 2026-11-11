import argparse
from pathlib import Path
from time import perf_counter

from app.db import get_connection
from app.parser import parse_line


def ingest_logs(path, replace_source=None):
    source_file = path.name
    schema_path = Path(__file__).with_name("schema.sql")

    if replace_source == source_file:
        raise ValueError("Replacement source must differ from the new source")

    count = 0
    start = perf_counter()

    with get_connection() as connection:
        connection.execute(schema_path.read_text(encoding="utf-8"))

        existing = connection.execute(
            "SELECT 1 FROM log_events WHERE source_file = %s LIMIT 1",
            (source_file,),
        ).fetchone()

        if existing:
            print(f"{source_file} is already imported. Skipping.")
            return

        if replace_source:
            cursor = connection.execute(
                "DELETE FROM log_events WHERE source_file = %s",
                (replace_source,),
            )
            print(f"Replacing {cursor.rowcount:,} rows from {replace_source}")

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

                        if count % 100_000 == 0:
                            print(f"Sent {count:,} events", flush=True)

    elapsed = perf_counter() - start

    print(f"Imported {count:,} events from {source_file}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print(f"Ingestion speed: {count / elapsed:,.0f} events/second")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import HDFS logs")
    parser.add_argument("path", type=Path)
    parser.add_argument("--replace-source")
    args = parser.parse_args()

    ingest_logs(args.path, args.replace_source)