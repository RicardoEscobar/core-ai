-- Given this table:
CREATE TABLE IF NOT EXISTS completion.completion
(
    id bigserial NOT NULL,
    prompt jsonb DEFAULT '["<|endoftext|>"]',
    suffix text,
    max_tokens integer DEFAULT 16,
    temperature numeric DEFAULT 1,
    top_p numeric DEFAULT 1,
    n integer DEFAULT 1,
    stream boolean DEFAULT false,
    logprobs integer,
    echo boolean DEFAULT false,
    stop jsonb,
    presence_penalty numeric DEFAULT 0,
    frequency_penalty numeric DEFAULT 0,
    best_of integer DEFAULT 1,
    logit_bias jsonb,
    model_id bigint NOT NULL,
    user_id bigint NOT NULL,
    PRIMARY KEY (id)
);

-- Create a stored procedure that will insert a new completion. And returns the id of the new completion.
CREATE OR REPLACE FUNCTION completion.insert_completion(prompt jsonb, suffix text, max_tokens integer, temperature numeric, top_p numeric, n integer, stream boolean, logprobs integer, echo boolean, stop jsonb, presence_penalty numeric, frequency_penalty numeric, best_of integer, logit_bias jsonb, model_id bigint, user_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        INSERT INTO completion.completion (prompt, suffix, max_tokens, temperature, top_p, n, stream, logprobs, echo, stop, presence_penalty, frequency_penalty, best_of, logit_bias, model_id, user_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        RETURNING id;
    $$;

-- Create a stored procedure that will update a completion. And returns the id of the updated completion.
CREATE OR REPLACE FUNCTION completion.update_completion(id bigint, prompt jsonb, suffix text, max_tokens integer, temperature numeric, top_p numeric, n integer, stream boolean, logprobs integer, echo boolean, stop jsonb, presence_penalty numeric, frequency_penalty numeric, best_of integer, logit_bias jsonb, model_id bigint, user_id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        UPDATE completion.completion
        SET prompt = $2, suffix = $3, max_tokens = $4, temperature = $5, top_p = $6, n = $7, stream = $8, logprobs = $9, echo = $10, stop = $11, presence_penalty = $12, frequency_penalty = $13, best_of = $14, logit_bias = $15, model_id = $16, user_id = $17
        WHERE id = $1
        RETURNING id;
    $$;

-- Create a stored procedure that will delete a completion. And returns the id of the deleted completion.
CREATE OR REPLACE FUNCTION completion.delete_completion(id bigint)
    RETURNS bigint
    LANGUAGE sql
    AS $$
        DELETE FROM completion.completion
        WHERE id = $1
        RETURNING id;
    $$;