ALTER TABLE IF EXISTS "user".user_account
    ADD CONSTRAINT user_account_account_id_fkey FOREIGN KEY (account_id)
    REFERENCES "user".account (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS "user".user_account
    ADD CONSTRAINT user_account_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES "user"."user" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;