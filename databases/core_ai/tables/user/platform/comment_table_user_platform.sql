COMMENT ON TABLE "user".platform
    IS 'Platform information, where the user is interacting with the AI.
The same user may create several accounts on the same or different platforms.';

COMMENT ON COLUMN "user".platform.name
    IS 'text
Required
Name of the platform.';

COMMENT ON COLUMN "user".platform.description
    IS 'text
Optional
Description of the platform.';