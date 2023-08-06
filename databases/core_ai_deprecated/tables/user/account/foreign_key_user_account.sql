/*
Foreign key for user_account table.
*/
ALTER TABLE IF EXISTS "user".account
    ADD CONSTRAINT account_platform_id_fkey FOREIGN KEY (platform_id)
    REFERENCES "user".platform (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;