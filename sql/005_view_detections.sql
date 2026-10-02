SELECT
    detection_type,
    source_ip,
    username,
    failed_attempts,
    severity,
    first_seen,
    last_seen,
    detected_at
FROM security_detections
ORDER BY
    failed_attempts DESC,
    detected_at DESC;

