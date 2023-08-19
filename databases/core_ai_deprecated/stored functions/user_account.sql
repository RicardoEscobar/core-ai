-- Given this table:
CREATE TABLE IF NOT EXISTS "user".account
(
    id bigserial NOT NULL,
    name text NOT NULL,
    platform_id bigint NOT NULL,
    PRIMARY KEY (id)
);

-- Create a stored procedure that will insert a new account. And returns the id of the new account.
CREATE OR REPLACE FUNCTION "user".insert_account(name text, platform_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO "user".account (name, platform_id)
        VALUES ($1, $2)
        RETURNING id;
    $$;

-- Create a stored procedure that will update an account. And returns the id of the updated account.
CREATE OR REPLACE FUNCTION "user".update_account(id bigint, name text, platform_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE "user".account
        SET name = $2, platform_id = $3
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a stored procedure that will delete an account. And returns the id of the deleted account.
CREATE OR REPLACE FUNCTION "user".delete_account(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM "user".account
        WHERE id = $1
        RETURNING id;
    $$;
