DROP TABLE IF EXISTS "user"."user" CASCADE;

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('"user".user', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "user".user;

CREATE TABLE IF NOT EXISTS "user"."user"
(
    id bigserial NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    PRIMARY KEY (id),
    UNIQUE (name, email)
);

COMMENT ON TABLE "user"."user"
    IS 'User catalog, used to identify the human who is making the requests.';

COMMENT ON COLUMN "user"."user".name
    IS 'string
Required
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';

