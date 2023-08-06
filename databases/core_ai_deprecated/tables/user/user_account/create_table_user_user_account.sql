/*
Create table user_account

This table represents a many-to-many relationship between users and accounts.
*/

CREATE TABLE IF NOT EXISTS "user".user_account
(
    user_id serial NOT NULL,
    account_id serial NOT NULL,
    CONSTRAINT user_account_pkey PRIMARY KEY (user_id, account_id)
);