DROP TABLE IF EXISTS "user".platform  CASCADE;

CREATE TABLE IF NOT EXISTS "user".platform
(
    id bigserial NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id),
    UNIQUE (name)
);

COMMENT ON TABLE "user".platform
    IS 'Platform information, where the user is interacting with the AI.
The same user may create several accounts on the same or different platforms.';

COMMENT ON COLUMN "user".platform.name
    IS 'text
Required
Name of the platform.';

COMMENT ON COLUMN "user".platform.description
    IS 'text
Optional
Description of the platform.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('"user".platform', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "user".platform;
