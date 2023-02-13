-- Database: core_ai_completion
-- Description: Create a PostgreSQL database to store openai.Completion.create method calls.

-- DROP DATABASE IF EXISTS core_ai_completion;

CREATE DATABASE core_ai
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_MX.UTF-8'
    LC_CTYPE = 'es_MX.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    TEMPLATE template0;
