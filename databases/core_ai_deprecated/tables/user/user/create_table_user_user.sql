/*
Create table user.user

This table contains the different users of the AI.

These users are meant to be humans, but they can be AI personas as well.

The combination of name and email must be unique.

id: The unique identifier for the user.
name: The name of the user.
email: The email of the user.
created_at: The date and time the user was created.

*/
CREATE TABLE IF NOT EXISTS "user"."user"
(
    id serial PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    created_at timestamp DEFAULT timezone('UTC'::text, now()),
    CONSTRAINT user_name_email_key UNIQUE (name, email)
);
