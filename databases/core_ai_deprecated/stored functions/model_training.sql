-- Given this table:
CREATE TABLE IF NOT EXISTS model.training
(
    id bigserial NOT NULL,
    data jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    model_id bigint,
    PRIMARY KEY (id)
);

-- Create a stored procedure that will insert a new training. And returns the id of the new training.
CREATE OR REPLACE FUNCTION model.insert_training(data jsonb, model_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO model.training (data, model_id)
        VALUES ($1, $2)
        RETURNING id;
    $$;

-- Create a stored procedure that will update a training. And returns the id of the updated training.
CREATE OR REPLACE FUNCTION model.update_training(id bigint, data jsonb, model_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE model.training
        SET data = $2, model_id = $3
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a stored procedure that will delete a training. And returns the id of the deleted training.
CREATE OR REPLACE FUNCTION model.delete_training(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM model.training
        WHERE id = $1
        RETURNING id;
    $$;