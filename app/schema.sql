CREATE TABLE IF NOT EXISTS log_events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_file TEXT NOT NULL,
    line_number INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    thread_id INTEGER NOT NULL,
    level TEXT NOT NULL,
    component TEXT NOT NULL,
    message TEXT NOT NULL,
    block_ids TEXT[] NOT NULL,

    UNIQUE (source_file, line_number)
);