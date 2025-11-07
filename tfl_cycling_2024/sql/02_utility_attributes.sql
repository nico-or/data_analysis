CREATE TABLE trips AS
    SELECT * from trips_raw;

-- Add route ID
ALTER TABLE trips
ADD COLUMN route_id VARCHAR;

UPDATE trips
SET route_id = format('{:09d}{:09d}', station_start_id, station_end_id);

-- Add duration in minutes
ALTER TABLE trips
ADD COLUMN duration_minutes DOUBLE;

UPDATE trips
SET duration_minutes = duration_ms/(1000 * 60);

-- Add round trip flag
ALTER TABLE trips
ADD COLUMN round_trip BOOL DEFAULT false;

UPDATE trips
SET round_trip = (station_start_id == station_end_id);