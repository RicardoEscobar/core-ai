/*
CREATE TABLE user.platform 

This table contains the different platforms to be used by the AI to interact with it's human users.

id: The unique identifier for the platform.
name: The name of the platform.
description: A description of the platform.
*/

CREATE TABLE IF NOT EXISTS "user".platform
(
    id smallserial PRIMARY KEY,
    name text NOT NULL,
    description text
);