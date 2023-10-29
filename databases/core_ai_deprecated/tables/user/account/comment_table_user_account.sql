COMMENT ON TABLE "user".account
    IS 'User catalog, used to identify who is making the requests.';

COMMENT ON COLUMN "user".account.name
    IS 'string
Required
A unique identifier representing your end-user account on a given platform, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';
