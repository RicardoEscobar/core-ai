ALTER TABLE IF EXISTS "fine-tunning".sample
    ADD FOREIGN KEY (summary_id)
    REFERENCES "fine-tunning".summary (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;


ALTER TABLE IF EXISTS "fine-tunning".sample
    ADD FOREIGN KEY (account_id)
    REFERENCES "user".account (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;


ALTER TABLE IF EXISTS "fine-tunning".sample
    ADD FOREIGN KEY (previous_sample_id)
    REFERENCES "fine-tunning".sample (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;


ALTER TABLE IF EXISTS "fine-tunning".sample
    ADD FOREIGN KEY (model_id)
    REFERENCES model.model (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE
    NOT VALID;