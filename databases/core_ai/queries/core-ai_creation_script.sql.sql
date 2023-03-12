-- user schema

DROP TABLE IF EXISTS "user".platform;

CREATE TABLE IF NOT EXISTS "user".platform
(
    id smallserial PRIMARY KEY,
    name text NOT NULL,
    description text
);

COMMENT ON TABLE "user".platform
    IS 'Platform information, where the user is interacting with the AI.
The same user may create several accounts on the same or different platforms.';

COMMENT ON COLUMN "user".platform.name
    IS 'text
Required
Name of the platform.';

COMMENT ON COLUMN "user".platform.description
    IS 'text
Optional
Description of the platform.';

DROP TABLE IF EXISTS "user".account;

CREATE TABLE IF NOT EXISTS "user".account
(
    id serial PRIMARY KEY,
    name text NOT NULL,
    platform_id smallserial NOT NULL,
    CONSTRAINT account_name_platform_id_key UNIQUE (name, platform_id)
);

COMMENT ON TABLE "user".account
    IS 'User catalog, used to identify who is making the requests.';

COMMENT ON COLUMN "user".account.name
    IS 'string
Required
A unique identifier representing your end-user account on a given platform, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';

DROP TABLE IF EXISTS "user"."user";

CREATE TABLE IF NOT EXISTS "user"."user"
(
    id serial PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    created_at timestamp DEFAULT timezone('UTC'::text, now()),
    CONSTRAINT user_name_email_key UNIQUE (name, email)
);

COMMENT ON TABLE "user"."user"
    IS 'User catalog, used to identify the human or AI persona who is making the requests.';

COMMENT ON COLUMN "user"."user".name
    IS 'string
Required
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';

DROP TABLE IF EXISTS "user".user_account;

CREATE TABLE IF NOT EXISTS "user".user_account
(
    user_id serial NOT NULL,
    account_id serial NOT NULL,
    CONSTRAINT user_account_pkey PRIMARY KEY (user_id, account_id)
);

-- Completion schema

DROP TABLE IF EXISTS completion.chat_request;

CREATE TABLE IF NOT EXISTS completion.chat_request
(
    id bigserial PRIMARY KEY,
    model text NOT NULL DEFAULT 'gpt-3.5-turbo',
    messages jsonb NOT NULL,
    temperature numeric(3, 2) DEFAULT 1,
    top_p numeric(3, 2) DEFAULT 1,
    n integer DEFAULT 1,
    stream boolean DEFAULT FALSE,
    stop text[],
    max_tokens integer,
    presence_penalty numeric(3, 2) DEFAULT 0,
    frequency_penalty numeric(3, 2) DEFAULT 0,
    logit_bias jsonb,
    "user" text,
    created_at timestamp DEFAULT timezone('UTC'::text, now()),
    user_id serial
);

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

DROP TABLE IF EXISTS completion.role;

CREATE TABLE IF NOT EXISTS completion.role
(
    id smallserial PRIMARY KEY,
    name text
);

COMMENT ON TABLE completion.role
    IS 'The main input is the messages parameter. Messages must be an array of message objects, where each object has a role (either "system", "user", or "assistant")

This table stores those roles.';

DROP TABLE IF EXISTS completion.content;

CREATE TABLE IF NOT EXISTS completion.content
(
    id bigserial PRIMARY KEY,
    message text,
    created_at timestamp DEFAULT timezone('UTC'::text, now()),
    role_id bigint,
    account_id serial,
    persona_id serial
);

COMMENT ON TABLE completion.content
    IS 'Content (the content of the message). Conversations can be as short as 1 message or fill many pages.';

-- persona schema

DROP TABLE IF EXISTS persona.persona;

CREATE TABLE IF NOT EXISTS persona.persona
(
    id serial PRIMARY KEY,
    name text NOT NULL,
    basic_personality text
);

COMMENT ON TABLE persona.persona
    IS 'This table contains the different personas to be used by the AI to interact with it''s human users.';


-- Foreign keys

ALTER TABLE IF EXISTS "user".account
    ADD CONSTRAINT account_platform_id_fkey FOREIGN KEY (platform_id)
    REFERENCES "user".platform (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;

ALTER TABLE IF EXISTS "user".user_account
    ADD CONSTRAINT user_account_account_id_fkey FOREIGN KEY (account_id)
    REFERENCES "user".account (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS "user".user_account
    ADD CONSTRAINT user_account_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES "user"."user" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS completion.chat_request
    ADD FOREIGN KEY (user_id)
    REFERENCES "user"."user" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS completion.content
    ADD FOREIGN KEY (role_id)
    REFERENCES completion.role (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;

ALTER TABLE IF EXISTS completion.content
    ADD FOREIGN KEY (account_id)
    REFERENCES "user".account (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;

ALTER TABLE IF EXISTS completion.content
    ADD FOREIGN KEY (persona_id)
    REFERENCES persona.persona (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;