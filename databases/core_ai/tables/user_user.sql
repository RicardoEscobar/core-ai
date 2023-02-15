DROP TABLE IF EXISTS "user"."user" CASCADE;

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

