ALTER TABLE IF EXISTS completion.chat_request
    ADD FOREIGN KEY (user_id)
    REFERENCES "user"."user" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;