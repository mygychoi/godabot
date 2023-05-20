-- Goda 2023-05-20
CREATE OR REPLACE FUNCTION refresh_updated_at() RETURNS trigger AS
$refresh_updated_at$
BEGIN
    NEW.updated_at := current_timestamp;
    RETURN NEW;
END;
$refresh_updated_at$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER access_access_refresh_updated_a
    BEFORE UPDATE
    ON access_access
    FOR EACH ROW
EXECUTE FUNCTION refresh_updated_at();
