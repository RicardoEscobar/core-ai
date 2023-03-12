CREATE TABLE IF NOT EXISTS completion.content
(
    id bigserial PRIMARY KEY,
    message text,
    created_at timestamp DEFAULT timezone('UTC'::text, now()),
    role_id bigint,
    account_id serial,
    persona_id serial
);