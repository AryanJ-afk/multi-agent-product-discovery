import re
from datetime import datetime


def parse_line(line):
    parts = line.strip().split(maxsplit=5)

    if len(parts) != 6:
        raise ValueError("Expected six log fields")

    date_text, time_text, thread_id, level, component, message = parts

    timestamp = datetime.strptime(
        f"{date_text} {time_text}",
        "%y%m%d %H%M%S",
    )

    block_ids = []

    for block_id in re.findall(r"blk_-?\d+", message):
        if block_id not in block_ids:
            block_ids.append(block_id)

    return {
        "timestamp": timestamp,
        "thread_id": int(thread_id),
        "level": level,
        "component": component.rstrip(":"),
        "message": message,
        "block_ids": block_ids,
    }