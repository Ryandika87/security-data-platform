import sys
from pathlib import Path

import psycopg2

sys.path.append(str(Path(__file__).resolve().parents[1]))

from extract.auth_log import extract_file


DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "security_platform",
    "user": "security",
    "password": "security_dev",
}


def load_events(events: list[dict]) -> None:
    connection = psycopg2.connect(**DB_CONFIG)

    try:
        with connection:
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO raw_events (
                        event_timestamp,
                        source,
                        event_type,
                        source_ip,
                        source_port,
                        destination_ip,
                        destination_port,
                        username,
                        status,
                        message,
                        raw_log
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                """

                for event in events:
                    cursor.execute(
                        insert_query,
                        (
                            event["event_timestamp"],
                            event["source"],
                            event["event_type"],
                            event["source_ip"],
                            event["source_port"],
                            event["destination_ip"],
                            event["destination_port"],
                            event["username"],
                            event["status"],
                            event["message"],
                            event["raw_log"],
                        ),
                    )

    finally:
        connection.close()


if __name__ == "__main__":
    events = extract_file("data/raw/auth.log")
    load_events(events)

    print(f"Loaded {len(events)} events into raw_events")

