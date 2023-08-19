COMMENT ON TABLE completion.chat_request
    IS 'Given a chat conversation, the model will return a chat completion response.

This table stores the created chat completions requests made.';

COMMENT ON COLUMN completion.chat_request.model
    IS 'model
string
Required
ID of the model to use. Currently, only gpt-3.5-turbo and gpt-3.5-turbo-0301 are supported.';

COMMENT ON COLUMN completion.chat_request.messages
    IS 'messages
array
Required
The messages to generate chat completions for, in the chat format.';

COMMENT ON COLUMN completion.chat_request.temperature
    IS 'temperature
number
Optional
Defaults to 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or top_p but not both.';

COMMENT ON COLUMN completion.chat_request.top_p
    IS 'top_p
number
Optional
Defaults to 1
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.';

COMMENT ON COLUMN completion.chat_request.n
    IS 'Integer
Optional
Defaults to 1
How many chat completion choices to generate for each input message.';

COMMENT ON COLUMN completion.chat_request.stream
    IS 'boolean
Optional
Defaults to false
If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.';

COMMENT ON COLUMN completion.chat_request.stop
    IS 'string or array
Optional
Defaults to null
Up to 4 sequences where the API will stop generating further tokens.';

COMMENT ON COLUMN completion.chat_request.max_tokens
    IS 'integer
Optional
Defaults to inf
The maximum number of tokens allowed for the generated answer. By default, the number of tokens the model can return will be (4096 - prompt tokens).';

COMMENT ON COLUMN completion.chat_request.presence_penalty
    IS 'number
Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model''s likelihood to talk about new topics.

See more information about frequency and presence penalties.
https://platform.openai.com/docs/api-reference/parameter-details';

COMMENT ON COLUMN completion.chat_request.frequency_penalty
    IS 'number
Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model''s likelihood to repeat the same line verbatim.

See more information about frequency and presence penalties.
https://platform.openai.com/docs/api-reference/parameter-details';

COMMENT ON COLUMN completion.chat_request."user"
    IS 'string
Optional
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';
