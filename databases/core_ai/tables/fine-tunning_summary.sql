DROP TABLE IF EXISTS "fine-tunning".summary CASCADE;

CREATE TABLE IF NOT EXISTS "fine-tunning".summary
(
    id bigserial NOT NULL,
    summary text,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    PRIMARY KEY (id)
);

COMMENT ON TABLE "fine-tunning".summary
    IS 'Collects summary text from a chatlog.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('fine-tunning.summary', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "fine-tunning".summary;
