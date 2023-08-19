-- Given this table:
CREATE TABLE IF NOT EXISTS model.model
(
    id bigserial NOT NULL,
    model text NOT NULL,
    description text,
    max_request integer NOT NULL,
    training_data_up_to date NOT NULL,
    PRIMARY KEY (id)
);

-- Create a stored procedure that will insert a new model. And returns the id of the new model.
CREATE OR REPLACE FUNCTION model.insert_model(model text, description text, max_request integer, training_data_up_to date)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO model.model (model, description, max_request, training_data_up_to)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
    $$;

-- Create a stored procedure that will update a model. And returns the id of the updated model.
CREATE OR REPLACE FUNCTION model.update_model(id bigint, model text, description text, max_request integer, training_data_up_to date)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE model.model
        SET model = $2, description = $3, max_request = $4, training_data_up_to = $5
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a stored procedure that will delete a model. And returns the id of the deleted model.
CREATE OR REPLACE FUNCTION model.delete_model(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM model.model
        WHERE id = $1
        RETURNING id;
    $$;
    