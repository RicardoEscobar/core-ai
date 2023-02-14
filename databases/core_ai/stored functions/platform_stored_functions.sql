
-- Given this table:
CREATE TABLE IF NOT EXISTS "user".platform
(
    id bigserial NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id)
);

-- Create a stored procedure that will insert a new platform. And returns the id of the new platform.
CREATE OR REPLACE FUNCTION "user".insert_platform(name text, description text)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO "user".platform (name, description)
        VALUES ($1, $2)
        RETURNING id;
    $$;