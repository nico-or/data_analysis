-- Remove too long (>120 minutes) and too short (< 1 minute with same start and end location) trips
DELETE FROM trips
WHERE
duration_minutes > 60
OR
(duration_minutes < 1 AND station_start_id == station_end_id);