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
    created_at timestamp with time zone DEFAULT now() AT TIME ZONE 'UTC',
    user_id serial
);