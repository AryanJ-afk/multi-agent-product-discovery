from app.db import get_connection


def get_block_events(block_id, limit=100):
    if not 1 <= limit <= 500:
        raise ValueError("Limit must be between 1 and 500")

    with get_connection() as connection:
        connection.execute("SET LOCAL statement_timeout = '5s'")

        cursor = connection.execute(
            """
            SELECT
                id,
                source_file,
                line_number,
                timestamp,
                level,
                component,
                message
            FROM log_events
            WHERE block_ids @> ARRAY[%s]::text[]
            ORDER BY timestamp, id
            LIMIT %s
            """,
            (block_id, limit + 1),
        )

        rows = cursor.fetchall()

    events = []

    for row in rows[:limit]:
        events.append({
            "id": row[0],
            "source_file": row[1],
            "line_number": row[2],
            "timestamp": row[3].isoformat(),
            "level": row[4],
            "component": row[5],
            "message": row[6],
        })

    return {
        "block_id": block_id,
        "returned_count": len(events),
        "truncated": len(rows) > limit,
        "events": events,
    }