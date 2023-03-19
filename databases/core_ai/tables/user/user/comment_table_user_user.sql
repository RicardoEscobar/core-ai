COMMENT ON TABLE "user"."user"
    IS 'User catalog, used to identify the human or AI persona who is making the requests.';

COMMENT ON COLUMN "user"."user".name
    IS 'string
Required
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';
