-- Given this table:
CREATE TABLE IF NOT EXISTS "user".user_account
(
    user_id bigint NOT NULL,
    account_id bigint NOT NULL,
    PRIMARY KEY (user_id, account_id)
);


-- Create a stored procedure that will insert a new user, account relationship. And returns the user_id, account_id of the new relationship.
CREATE OR REPLACE FUNCTION "user".insert_user_account(user_id bigint, account_id bigint)
    RETURNS record
    LANGUAGE sql
    AS $$
        INSERT INTO "user".user_account (user_id, account_id)
        VALUES ($1, $2)
        RETURNING user_id, account_id;
    $$;

-- Create a stored procedure that will update a user, account relationship. And returns the user_id, account_id of the updated relationship.
CREATE OR REPLACE FUNCTION "user".update_user_account(user_id bigint, account_id bigint, new_account_id bigint, new_user_id bigint)
    RETURNS record
    LANGUAGE sql
    AS $$
        UPDATE "user".user_account
        SET user_id = $1, account_id = $2
        WHERE user_id = $3 AND account_id = $4
        RETURNING user_id, account_id;
    $$;

-- Create a stored procedure that will delete a user, account relationship. And returns the user_id, account_id of the deleted relationship.
CREATE OR REPLACE FUNCTION "user".delete_user_account(user_id bigint, account_id bigint)
    RETURNS record
    LANGUAGE sql
    AS $$
        DELETE FROM "user".user_account
        WHERE user_id = $1 AND account_id = $2
        RETURNING user_id, account_id;
    $$;