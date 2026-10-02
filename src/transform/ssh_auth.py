import sys
from pathlib import Path

import psycopg2

sys.path.append(str(Path(__file__).resolve().parents[2]))


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "security_platform",
    "user": "security",
    "password": "security_dev",
}


CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS ssh_auth_summary (
    source_ip INET NOT NULL,
    username VARCHAR(255) NOT NULL,

    total_attempts INTEGER NOT NULL,
    failed_attempts INTEGER NOT NULL,
    successful_attempts INTEGER NOT NULL,

    first_seen TIMESTAMPTZ,
    last_seen TIMESTAMPTZ,

    PRIMARY KEY (source_ip, username)
);
"""


TRANSFORM_QUERY = """
INSERT INTO ssh_auth_summary (
    source_ip,
    username,
    total_attempts,
    failed_attempts,
    successful_attempts,
    first_seen,
    last_seen
)
SELECT
    source_ip,
    username,
    COUNT(*) AS total_attempts,

    COUNT(*) FILTER (
        WHERE status = 'failed'
    ) AS failed_attempts,

    COUNT(*) FILTER (
        WHERE status = 'success'
    ) AS successful_attempts,

    MIN(event_timestamp) AS first_seen,
    MAX(event_timestamp) AS last_seen

FROM raw_events

WHERE event_type = 'ssh_auth'

GROUP BY
    source_ip,
    username

ON CONFLICT (source_ip, username)
DO UPDATE SET
    total_attempts = EXCLUDED.total_attempts,
    failed_attempts = EXCLUDED.failed_attempts,
    successful_attempts = EXCLUDED.successful_attempts,
    first_seen = EXCLUDED.first_seen,
    last_seen = EXCLUDED.last_seen;
"""


def transform() -> None:
    connection = psycopg2.connect(**DB_CONFIG)

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLE_QUERY)
                cursor.execute(TRANSFORM_QUERY)

    finally:
        connection.close()


if __name__ == "__main__":
    transform()
    print("SSH authentication data transformed successfully")

