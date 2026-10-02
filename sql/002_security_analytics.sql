-- SSH authentication activity
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

ORDER BY
    failed_attempts DESC,
    total_attempts DESC;
