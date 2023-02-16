DROP TABLE IF EXISTS model.model  CASCADE;

CREATE TABLE IF NOT EXISTS model.model
(
    id bigserial NOT NULL,
    model text NOT NULL,
    description text,
    max_request integer NOT NULL,
    training_data_up_to date NOT NULL,
    PRIMARY KEY (id)
);

COMMENT ON TABLE model.model
    IS 'List and describe the various models available in the API. You can refer to the Models documentation to understand what models are available and the differences between them.';

COMMENT ON COLUMN model.model.model
    IS 'string
Required
A unique identifier representing the actual model name.';

COMMENT ON COLUMN model.model.description
    IS 'string
Optional
Description of the model.';

COMMENT ON COLUMN model.model.max_request
    IS 'integer
Required
Maximun amount of tokens to be used per request for the model in question.
When creating requets, the prompt and response tokens are added up, and need to be equal or lesser than this amount.';

COMMENT ON COLUMN model.model.training_data_up_to
    IS 'date
Required
Last date when the training data is up to in UTC.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('model.model', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM model.model;
