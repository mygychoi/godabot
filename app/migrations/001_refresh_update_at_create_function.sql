-- Goda 2023.05.20

CREATE OR REPLACE FUNCTION refresh_updated_at() RETURNS trigger AS
$refresh_updated_at$
BEGIN
    NEW.updated_at := current_timestamp;
    RETURN NEW;
END;
$refresh_updated_at$ LANGUAGE plpgsql;
