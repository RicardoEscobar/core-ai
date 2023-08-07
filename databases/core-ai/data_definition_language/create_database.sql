-- Database: core-ai

-- DROP DATABASE IF EXISTS "core-ai";

CREATE DATABASE "core-ai"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "core-ai"
    IS 'This database stores chat messages between users and AI assistants.';