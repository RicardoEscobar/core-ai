ALTER TABLE IF EXISTS "user".user_account
    ADD FOREIGN KEY (user_id)
    REFERENCES "user"."user" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS "user".user_account
    ADD FOREIGN KEY (account_id)
    REFERENCES "user".account (id) MATCH SIMPLE
    ON UPDATE CASCADE 
    ON DELETE CASCADE
    NOT VALID;