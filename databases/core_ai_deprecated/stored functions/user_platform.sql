
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

-- Create a stored procedure that will update a platform. And returns the id of the updated platform.
CREATE OR REPLACE FUNCTION "user".update_platform(id bigint, name text, description text)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE "user".platform
        SET name = $2, description = $3
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a stored procedure that will delete a platform. And returns the id of the deleted platform.
CREATE OR REPLACE FUNCTION "user".delete_platform(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM "user".platform
        WHERE id = $1
        RETURNING id;
    $$;
