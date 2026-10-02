import re
from datetime import datetime
from zoneinfo import ZoneInfo


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+"
    r"(?P<service>\S+)\[(?P<pid>\d+)\]:\s+"
    r"(?P<message>.*)$"
)

AUTH_PATTERN = re.compile(
    r"^(?P<action>Failed|Accepted)\s+"
    r"(?P<method>password|publickey)\s+for\s+"
    r"(?P<username>\S+)\s+from\s+"
    r"(?P<source_ip>\S+)\s+port\s+"
    r"(?P<source_port>\d+)"
)


def parse_timestamp(timestamp: str) -> datetime:
    dt = datetime.strptime(
        f"2026 {timestamp}",
        "%Y %b %d %H:%M:%S",
    )

    return dt.replace(tzinfo=ZoneInfo("Asia/Jakarta"))


def parse_line(line: str) -> dict | None:
    line = line.strip()

    if not line:
        return None

    match = LOG_PATTERN.match(line)

    if not match:
        return None

    timestamp = parse_timestamp(match.group("timestamp"))
    message = match.group("message")

    auth_match = AUTH_PATTERN.match(message)

    if not auth_match:
        return {
            "event_timestamp": timestamp,
            "source": "auth.log",
            "event_type": "unknown",
            "source_ip": None,
            "source_port": None,
            "destination_ip": None,
            "destination_port": None,
            "username": None,
            "status": None,
            "message": message,
            "raw_log": line,
        }

    action = auth_match.group("action")
    method = auth_match.group("method")

    status = "failed" if action == "Failed" else "success"

    return {
        "event_timestamp": timestamp,
        "source": "auth.log",
        "event_type": "ssh_auth",
        "source_ip": auth_match.group("source_ip"),
        "source_port": int(auth_match.group("source_port")),
        "destination_ip": None,
        "destination_port": 22,
        "username": auth_match.group("username"),
        "status": status,
        "message": message,
        "raw_log": line,
    }


def extract_file(path: str) -> list[dict]:
    events = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            event = parse_line(line)

            if event is not None:
                events.append(event)

    return events


if __name__ == "__main__":
    events = extract_file("data/raw/auth.log")

    for event in events:
        print(event)
