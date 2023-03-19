CREATE TABLE IF NOT EXISTS persona.persona
(
    id serial PRIMARY KEY,
    name text NOT NULL,
    basic_personality text
);