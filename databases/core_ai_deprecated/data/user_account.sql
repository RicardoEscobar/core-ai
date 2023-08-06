-- Path: databases\core_ai\data\user_account.sql
-- This file inserts the default data into the user.account table.

INSERT INTO "user".account (name, platform_id)
VALUES
('Jorge', (SELECT id FROM "user".platform WHERE name = $$Core AI$$)),
('JorgeEscobar', (SELECT id FROM "user".platform WHERE name = $$VRChat$$))
ON CONFLICT (name, platform_id) DO NOTHING;
