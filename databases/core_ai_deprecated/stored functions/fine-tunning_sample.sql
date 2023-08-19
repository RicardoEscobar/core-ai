-- Given this table:
CREATE TABLE IF NOT EXISTS "fine-tunning".sample
(
    id bigserial NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    prompt text,
    response text,
    previous_sample_id bigint,
    summary_id bigint,
    account_id bigint NOT NULL,
    model_id bigint NOT NULL,
    PRIMARY KEY (id)
);

-- Create a function that will insert a new sample. And returns the id of the new sample.
CREATE OR REPLACE FUNCTION "fine-tunning".insert_sample(prompt text, response text, previous_sample_id bigint, summary_id bigint, account_id bigint, model_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO "fine-tunning".sample (prompt, response, previous_sample_id, summary_id, account_id, model_id)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
    $$;

-- Create a function that will update a sample. And returns the id of the updated sample.
CREATE OR REPLACE FUNCTION "fine-tunning".update_sample(id bigint, prompt text, response text, previous_sample_id bigint, summary_id bigint, account_id bigint, model_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE "fine-tunning".sample
        SET prompt = $2, response = $3, previous_sample_id = $4, summary_id = $5, account_id = $6, model_id = $7
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a function that will delete a sample. And returns the id of the deleted sample.
CREATE OR REPLACE FUNCTION "fine-tunning".delete_sample(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM "fine-tunning".sample
        WHERE id = $1
        RETURNING id;
    $$;