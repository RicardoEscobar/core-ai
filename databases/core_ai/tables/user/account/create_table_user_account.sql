/*
Create table user.account
This table contains the different user accounts on different platforms.

I make a distinction betrween user accounts and users themselves, they are not the same to me.

A user can have multiple accounts on different platforms, but an account can only belong to one user.

This table is used to identify the user making the request to the API.

The user_id column is used to identify the user making the request to the API.

The platform_id column is used to identify the platform the user is using to make the request to the API.

The name column is used to identify the user account on the platform the user is using to make the request to the API.

The name column is a unique identifier representing the end-user account on a given platform, which can help OpenAI to monitor and detect abuse.

The combination of the name and platform_id columns is unique.

id: The unique identifier for the user account.
name: The name of the user account.
platform_id: The unique identifier for the platform the user account belongs to.
*/

CREATE TABLE IF NOT EXISTS "user".account
(
    id serial PRIMARY KEY,
    name text NOT NULL,
    platform_id smallserial NOT NULL,
    CONSTRAINT account_name_platform_id_key UNIQUE (name, platform_id)
);