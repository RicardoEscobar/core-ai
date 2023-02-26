DROP TABLE IF EXISTS "user".user_account;

CREATE TABLE IF NOT EXISTS "user".user_account
(
    user_id bigint NOT NULL,
    account_id bigint NOT NULL,
    PRIMARY KEY (user_id, account_id)
);
