DROP TABLE IF EXISTS "fine-tunning".sample CASCADE;

CREATE TABLE IF NOT EXISTS "fine-tunning".sample
(
    id bigserial NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT (NOW() AT TIME ZONE 'UTC'),
    prompt text,
    response text,
    previous_sample_id bigint,
    summary_id bigint,
    account_id bigint NOT NULL,
    model_id bigint NOT NULL,
    PRIMARY KEY (id)
);

COMMENT ON TABLE "fine-tunning".sample
    IS 'A chatbot will normally contain relevant context about the conversation ( psychological profile), summary of the conversation so far as well as most recent messages. For this use case the same past conversation can generate multiple rows in the dataset, each time with a slightly different context, for every agent generation as a completion. This use case will require a few thousand examples, as it will likely deal with different types of requests, and user issues. To ensure the performance is of high quality we recommend vetting the conversation samples to ensure the quality of agent messages. The summary can be generated with a separate text transformation fine tuned model. The dataset could look as follows:

{"prompt":"Summary: <summary of the interaction so far>\n\nSpecific information:<for example order details in natural language>\n\n###\n\nUser: <message1>\nWaifu: <response1>\nUser: <message2>\nWaifu:", "completion":" <response2>\n"}
{"prompt":"Summary: <summary of the interaction so far>\n\nSpecific information:<for example order details in natural language>\n\n###\n\nUser: <message1>\nWaifu: <response1>\nUser: <message2>\nWaifu: <response2>\nCustomer: <message3>\nWaifu:", "completion":" <response3>\n"}';

COMMENT ON COLUMN "fine-tunning".sample.model_id
    IS 'bigint
required
Agent is an instance of a model or a fine-tuned model that is answering this chat.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('fine-tunning.sample', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "fine-tunning".sample;
