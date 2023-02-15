DROP TABLE IF EXISTS "user".account  CASCADE;

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('"user".account', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "user".account;

CREATE TABLE IF NOT EXISTS "user".account
(
    id bigserial NOT NULL,
    name text NOT NULL,
    platform_id bigint NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name, platform_id)
);

COMMENT ON TABLE "user".account
    IS 'User catalog, used to identify who is making the requests.';

COMMENT ON COLUMN "user".account.name
    IS 'string
Required
A unique identifier representing your end-user account on a given platform, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';