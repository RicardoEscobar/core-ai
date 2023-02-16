DROP TABLE IF EXISTS completion.completion CASCADE;

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

COMMENT ON TABLE completion.completion
    IS 'Given a prompt, the model will return one or more predicted completions, and can also return the probabilities of alternative tokens at each position.

This table stores completions and it''s attributes.';

COMMENT ON COLUMN completion.completion.prompt
    IS 'string or array
Optional
Defaults to <|endoftext|>
The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.

Note that <|endoftext|> is the document separator that the model sees during training, so if a prompt is not specified the model will generate as if from the beginning of a new document.';

COMMENT ON COLUMN completion.completion.suffix
    IS 'string
Optional
Defaults to null
The suffix that comes after a completion of inserted text.';

COMMENT ON COLUMN completion.completion.max_tokens
    IS 'integer
Optional
Defaults to 16
The maximum number of tokens to generate in the completion.

The token count of your prompt plus max_tokens cannot exceed the model''s context length. Most models have a context length of 2048 tokens (except for the newest models, which support 4096).';

COMMENT ON COLUMN completion.completion.temperature
    IS 'number
Optional
Defaults to 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or top_p but not both.';

COMMENT ON COLUMN completion.completion.top_p
    IS 'number
Optional
Defaults to 1
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.';

COMMENT ON COLUMN completion.completion.n
    IS 'integer
Optional
Defaults to 1
How many completions to generate for each prompt.

Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for max_tokens and stop.';

COMMENT ON COLUMN completion.completion.stream
    IS 'boolean
Optional
Defaults to false
Whether to stream back partial progress. If set, tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.';

COMMENT ON COLUMN completion.completion.logprobs
    IS 'integer
Optional
Defaults to null
Include the log probabilities on the logprobs most likely tokens, as well the chosen tokens. For example, if logprobs is 5, the API will return a list of the 5 most likely tokens. The API will always return the logprob of the sampled token, so there may be up to logprobs+1 elements in the response.

The maximum value for logprobs is 5. If you need more than this, please contact us through our Help center and describe your use case.';

COMMENT ON COLUMN completion.completion.echo
    IS 'boolean
Optional
Defaults to false
Echo back the prompt in addition to the completion';

COMMENT ON COLUMN completion.completion.stop
    IS 'string or array
Optional
Defaults to null
Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.';

COMMENT ON COLUMN completion.completion.presence_penalty
    IS 'number
Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model''s likelihood to talk about new topics.

See more information about frequency and presence penalties.
https://platform.openai.com/docs/api-reference/parameter-details';

COMMENT ON COLUMN completion.completion.frequency_penalty
    IS 'number
Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model''s likelihood to repeat the same line verbatim.
See more information about frequency and presence penalties.
https://platform.openai.com/docs/api-reference/parameter-details';

COMMENT ON COLUMN completion.completion.best_of
    IS 'integer
Optional
Defaults to 1
Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.

When used with n, best_of controls the number of candidate completions and n specifies how many to return – best_of must be greater than n.

Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for max_tokens and stop.';

COMMENT ON COLUMN completion.completion.logit_bias
    IS 'map
Optional
Defaults to null
Modify the likelihood of specified tokens appearing in the completion.

Accepts a json object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. You can use this tokenizer tool (which works for both GPT-2 and GPT-3) to convert text to token IDs. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

As an example, you can pass {"50256": -100} to prevent the <|endoftext|> token from being generated.

The json and jsonb data types accept almost identical sets of values as input. The major practical difference is one of efficiency. The json data type stores an exact copy of the input text, which processing functions must reparse on each execution; while jsonb data is stored in a decomposed binary format that makes it slightly slower to input due to added conversion overhead, but significantly faster to process, since no reparsing is needed. jsonb also supports indexing, which can be a significant advantage.

https://www.postgresql.org/docs/current/datatype-json.html';

COMMENT ON COLUMN completion.completion.model_id
    IS 'Links to string
Required
ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.';

COMMENT ON COLUMN completion.completion.user_id
    IS 'Links to string
Required
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('completion.completion', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM completion.completion;
