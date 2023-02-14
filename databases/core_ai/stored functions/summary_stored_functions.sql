-- Given this table:
CREATE TABLE IF NOT EXISTS "fine-tunning".summary
(
    id bigserial NOT NULL,
    summary text,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    PRIMARY KEY (id)
);

-- Create a function that will insert a new summary. And returns the id of the new summary.
CREATE OR REPLACE FUNCTION "fine-tunning".insert_summary(summary text)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO "fine-tunning".summary (summary)
        VALUES ($1)
        RETURNING id;
    $$;

-- Create a function that will update a summary. And returns the id of the updated summary.
CREATE OR REPLACE FUNCTION "fine-tunning".update_summary(id bigint, summary text)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE "fine-tunning".summary
        SET summary = $2
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a function that will delete a summary. And returns the id of the deleted summary.
CREATE OR REPLACE FUNCTION "fine-tunning".delete_summary(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM "fine-tunning".summary
        WHERE id = $1
        RETURNING id;
    $$;