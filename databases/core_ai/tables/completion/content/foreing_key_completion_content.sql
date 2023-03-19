ALTER TABLE IF EXISTS completion.content
    ADD FOREIGN KEY (role_id)
    REFERENCES completion.role (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;


ALTER TABLE IF EXISTS completion.content
    ADD FOREIGN KEY (account_id)
    REFERENCES "user".account (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS completion.content
    ADD FOREIGN KEY (persona_id)
    REFERENCES persona.persona (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    NOT VALID;