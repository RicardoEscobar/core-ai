DROP TABLE IF EXISTS model.training CASCADE;

CREATE TABLE IF NOT EXISTS model.training
(
    id bigserial NOT NULL,
    data jsonb,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    model_id bigint,
    PRIMARY KEY (id)
);

COMMENT ON TABLE model.training
    IS 'Training data is how you teach GPT-3 what you''d like it to say.

Your data must be a JSONL document, where each line is a prompt-completion pair corresponding to a training example. You can use our CLI data preparation tool to easily convert your data into this file format.';

COMMENT ON COLUMN model.training.data
    IS 'jasonb
Optional
In PostgreSQL, each of these entries should be stored as JSONB data types.
Examples:

{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
...

In PostgreSQL:

training_data = ''{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}''::jsonb';

COMMENT ON COLUMN model.training.model_id
    IS 'bigint
Required
This is a reference to the model that this training data belongs to.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('model.training', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM model.training;
