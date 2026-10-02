CREATE TABLE IF NOT EXISTS security_detections (
    id BIGSERIAL PRIMARY KEY,

    detection_type VARCHAR(100) NOT NULL,

    source_ip INET NOT NULL,
    username VARCHAR(255),

    failed_attempts INTEGER NOT NULL,

    first_seen TIMESTAMPTZ,
    last_seen TIMESTAMPTZ,

    severity VARCHAR(20) NOT NULL,

    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

