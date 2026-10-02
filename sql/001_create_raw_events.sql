CREATE TABLE IF NOT EXISTS raw_events (
    id BIGSERIAL PRIMARY KEY,

    event_timestamp TIMESTAMPTZ,
    source VARCHAR(50),
    event_type VARCHAR(100),

    source_ip INET,
    source_port INTEGER,

    destination_ip INET,
    destination_port INTEGER,

    username VARCHAR(255),

    status VARCHAR(50),

    message TEXT,

    raw_log TEXT,

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
