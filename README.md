# Security Data Platform

A small security data pipeline built with Python, PostgreSQL, and Docker.

The project currently focuses on processing SSH authentication logs. The logs are extracted, stored as raw events, transformed into structured data, and then used for basic security analysis and brute-force detection.

This project is still being developed. More security data sources and detection methods will be added later.

## Current Pipeline

```text
auth.log
   |
   v
Python Extractor
   |
   v
raw_events
   |
   v
SSH Authentication Transform
   |
   v
ssh_auth_summary
   |
   +------> Security Analytics
   |
   v
Brute-force Detection
   |
   v
security_detections
```

## Tech Stack

- Python 3
- PostgreSQL 16
- Docker
- Docker Compose
- psycopg2
- Git

## Project Structure

```text
security-data-platform/
├── data/
│   └── raw/
│       └── auth.log
│
├── docker/
│   └── postgres/
│
├── docs/
│
├── sql/
│   ├── 001_create_raw_events.sql
│   ├── 002_security_analytics.sql
│   ├── 003_create_detections.sql
│   ├── 004_detect_bruteforce.sql
│   └── 005_view_detections.sql
│
├── src/
│   ├── extract/
│   │   └── auth_log.py
│   │
│   ├── load/
│   │   └── postgres.py
│   │
│   └── transform/
│       └── ssh_auth.py
│
├── tests/
│
├── docker-compose.yml
└── README.md
```

## Setup

### 1. Start PostgreSQL

Start the PostgreSQL container with Docker Compose:

```bash
docker compose up -d
```

PostgreSQL is exposed on port `5433` on the host.

Database configuration used by the project:

```text
Database: security_platform
User:     security
Password: security_dev
Port:     5433
```

These credentials are only for local development.

### 2. Create the database table

Run the initial schema:

```bash
docker compose exec -T postgres \
  psql -U security -d security_platform \
  < sql/001_create_raw_events.sql
```

### 3. Set up the Python environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the PostgreSQL driver:

```bash
pip install psycopg2-binary
```

## Running the Pipeline

### Extract

The extractor reads the sample SSH authentication log and converts each log line into a structured event.

```bash
python src/extract/auth_log.py
```

The current sample contains 7 SSH authentication events.

### Load

Load the extracted events into PostgreSQL:

```bash
python src/load/postgres.py
```

The events are stored in the `raw_events` table.

### Transform

Transform the raw SSH authentication events into an aggregated table:

```bash
python src/transform/ssh_auth.py
```

The result is stored in:

```text
ssh_auth_summary
```

The table contains information such as:

- source IP
- username
- total authentication attempts
- failed attempts
- successful attempts
- first seen
- last seen

## Security Analytics

The project also contains SQL queries for analyzing SSH authentication activity.

Run:

```bash
docker compose exec -T postgres \
  psql -U security -d security_platform \
  < sql/002_security_analytics.sql
```

This groups authentication activity by source IP and username.

## Brute-force Detection

The current detection rule looks for sources with at least 3 failed SSH authentication attempts.

Create the detection table:

```bash
docker compose exec -T postgres \
  psql -U security -d security_platform \
  < sql/003_create_detections.sql
```

Run the detection:

```bash
docker compose exec -T postgres \
  psql -U security -d security_platform \
  < sql/004_detect_bruteforce.sql
```

View the detection results:

```bash
docker compose exec -T postgres \
  psql -U security -d security_platform \
  < sql/005_view_detections.sql
```

The current sample data contains repeated failed authentication attempts from several IP addresses. The detection query identifies sources that reach the configured threshold.

## Current Detection Rule

| Failed Attempts | Severity |
|---:|---|
| 1–2 | Not detected |
| 3–4 | Medium |
| 5+ | High |

This is only a simple rule for the current prototype. It is not intended to represent a production SOC detection rule yet.

## Planned Work

The project will be developed further in several stages.

Some of the planned work includes:

- improve the ETL process
- add data validation and tests
- handle duplicate events
- make the pipeline easier to run repeatedly
- introduce dbt
- add Airflow for orchestration
- enrich security events with additional information
- add more detection rules
- connect the pipeline with simulated attacks
- build a dashboard for security events

The exact implementation may change as the project develops.

## Notes

The current log file is a small manually prepared dataset for development and testing.

Some fields, such as the destination IP address, are not available in the sample SSH log and are therefore left empty. The destination port is set to `22` based on the SSH service.

The current timestamp parser also uses the year `2026` and the `Asia/Jakarta` timezone because the sample log does not contain a year or timezone.

This is a development project, not a production security monitoring system.
