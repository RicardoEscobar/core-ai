-- Given this table:
CREATE TABLE IF NOT EXISTS "user"."user"
(
    id bigserial NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    PRIMARY KEY (id),
    UNIQUE (name, email)
);

-- Create a stored function that will insert a new user. And returns the id of the new user.
CREATE OR REPLACE FUNCTION "user".insert_user(name text, email text)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO "user"."user" (name, email)
        VALUES ($1, $2)
        RETURNING id;
    $$;

-- Create a stored function that will update a user. And returns the id of the updated user.
CREATE OR REPLACE FUNCTION "user".update_user(id bigint, name text, email text)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE "user"."user"
        SET name = $2, email = $3
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a stored function that will delete a user. And returns the id of the deleted user.
CREATE OR REPLACE FUNCTION "user".delete_user(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM "user"."user"
        WHERE id = $1
        RETURNING id;
    $$;