TRUNCATE TABLE security_detections;

INSERT INTO security_detections (
    detection_type,
    source_ip,
    username,
    failed_attempts,
    first_seen,
    last_seen,
    severity
)
SELECT
    'ssh_bruteforce' AS detection_type,
    source_ip,
    username,
    failed_attempts,
    first_seen,
    last_seen,

    CASE
        WHEN failed_attempts >= 5 THEN 'high'
        WHEN failed_attempts >= 3 THEN 'medium'
        ELSE 'low'
    END AS severity

FROM ssh_auth_summary

WHERE failed_attempts >= 3;
