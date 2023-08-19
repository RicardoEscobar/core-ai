-- This file inserts the default data into the user.platform table.

INSERT INTO "user".platform (name, description)
VALUES 
('Core AI','Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.'),
('VRChat','VRChat is a social VR platform where users can create and share their own virtual worlds, avatars, and experiences.')
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description
RETURNING *;