--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.1

-- Started on 2023-02-15 12:37:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET SESSION AUTHORIZATION 'postgres';

DROP DATABASE "core_ai";
--
-- TOC entry 3443 (class 1262 OID 25396)
-- Name: core_ai; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "core_ai" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es_MX.UTF-8';


\connect "core_ai"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET SESSION AUTHORIZATION 'postgres';

--
-- TOC entry 8 (class 2615 OID 25399)
-- Name: completion; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "completion";


--
-- TOC entry 3444 (class 0 OID 0)
-- Dependencies: 8
-- Name: SCHEMA "completion"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "completion" IS 'Completion schema, to store data about completion requests.';


--
-- TOC entry 9 (class 2615 OID 25400)
-- Name: fine-tunning; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "fine-tunning";


--
-- TOC entry 3445 (class 0 OID 0)
-- Dependencies: 9
-- Name: SCHEMA "fine-tunning"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "fine-tunning" IS 'Fine-tuning lets you get more out of the models available through the API by providing:

Higher quality results than prompt design
Ability to train on more examples than can fit in a prompt
Token savings due to shorter prompts
Lower latency requests
GPT-3 has been pre-trained on a vast amount of text from the open internet. When given a prompt with just a few examples, it can often intuit what task you are trying to perform and generate a plausible completion. This is often called "few-shot learning."

Fine-tuning improves on few-shot learning by training on many more examples than can fit in the prompt, letting you achieve better results on a wide number of tasks. Once a model has been fine-tuned, you won''t need to provide examples in the prompt anymore. This saves costs and enables lower-latency requests.

At a high level, fine-tuning involves the following steps:

Prepare and upload training data
Train a new fine-tuned model
Use your fine-tuned model';


--
-- TOC entry 7 (class 2615 OID 25398)
-- Name: model; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "model";


--
-- TOC entry 3446 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA "model"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "model" IS 'Model schema for handling model information.';


SET SESSION AUTHORIZATION 'pg_database_owner';

--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA "public"; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA "public" IS 'standard public schema';


SET SESSION AUTHORIZATION 'postgres';

--
-- TOC entry 6 (class 2615 OID 25397)
-- Name: user; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "user";


--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA "user"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "user" IS 'User schema for handling identity and user data.';


--
-- TOC entry 271 (class 1255 OID 34080)
-- Name: delete_completion(bigint); Type: FUNCTION; Schema: completion; Owner: postgres
--

CREATE FUNCTION "completion"."delete_completion"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM completion.completion
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 240 (class 1255 OID 34078)
-- Name: insert_completion("jsonb", "text", integer, numeric, numeric, integer, boolean, integer, boolean, "jsonb", numeric, numeric, integer, "jsonb", bigint, bigint); Type: FUNCTION; Schema: completion; Owner: postgres
--

CREATE FUNCTION "completion"."insert_completion"("prompt" "jsonb", "suffix" "text", "max_tokens" integer, "temperature" numeric, "top_p" numeric, "n" integer, "stream" boolean, "logprobs" integer, "echo" boolean, "stop" "jsonb", "presence_penalty" numeric, "frequency_penalty" numeric, "best_of" integer, "logit_bias" "jsonb", "model_id" bigint, "user_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO completion.completion (prompt, suffix, max_tokens, temperature, top_p, n, stream, logprobs, echo, stop, presence_penalty, frequency_penalty, best_of, logit_bias, model_id, user_id)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        RETURNING id;
    $_$;


--
-- TOC entry 270 (class 1255 OID 34079)
-- Name: update_completion(bigint, "jsonb", "text", integer, numeric, numeric, integer, boolean, integer, boolean, "jsonb", numeric, numeric, integer, "jsonb", bigint, bigint); Type: FUNCTION; Schema: completion; Owner: postgres
--

CREATE FUNCTION "completion"."update_completion"("id" bigint, "prompt" "jsonb", "suffix" "text", "max_tokens" integer, "temperature" numeric, "top_p" numeric, "n" integer, "stream" boolean, "logprobs" integer, "echo" boolean, "stop" "jsonb", "presence_penalty" numeric, "frequency_penalty" numeric, "best_of" integer, "logit_bias" "jsonb", "model_id" bigint, "user_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE completion.completion
        SET prompt = $2, suffix = $3, max_tokens = $4, temperature = $5, top_p = $6, n = $7, stream = $8, logprobs = $9, echo = $10, stop = $11, presence_penalty = $12, frequency_penalty = $13, best_of = $14, logit_bias = $15, model_id = $16, user_id = $17
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 269 (class 1255 OID 27723)
-- Name: delete_sample(bigint); Type: FUNCTION; Schema: fine-tunning; Owner: postgres
--

CREATE FUNCTION "fine-tunning"."delete_sample"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM "fine-tunning".sample
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 245 (class 1255 OID 25894)
-- Name: delete_summary(bigint); Type: FUNCTION; Schema: fine-tunning; Owner: postgres
--

CREATE FUNCTION "fine-tunning"."delete_summary"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM "fine-tunning".summary
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 267 (class 1255 OID 27721)
-- Name: insert_sample("text", "text", bigint, bigint, bigint, bigint); Type: FUNCTION; Schema: fine-tunning; Owner: postgres
--

CREATE FUNCTION "fine-tunning"."insert_sample"("prompt" "text", "response" "text", "previous_sample_id" bigint, "summary_id" bigint, "account_id" bigint, "model_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO "fine-tunning".sample (prompt, response, previous_sample_id, summary_id, account_id, model_id)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
    $_$;


--
-- TOC entry 244 (class 1255 OID 25892)
-- Name: insert_summary("text"); Type: FUNCTION; Schema: fine-tunning; Owner: postgres
--

CREATE FUNCTION "fine-tunning"."insert_summary"("summary" "text") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO "fine-tunning".summary (summary)
        VALUES ($1)
        RETURNING id;
    $_$;


--
-- TOC entry 268 (class 1255 OID 27722)
-- Name: update_sample(bigint, "text", "text", bigint, bigint, bigint, bigint); Type: FUNCTION; Schema: fine-tunning; Owner: postgres
--

CREATE FUNCTION "fine-tunning"."update_sample"("id" bigint, "prompt" "text", "response" "text", "previous_sample_id" bigint, "summary_id" bigint, "account_id" bigint, "model_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE "fine-tunning".sample
        SET prompt = $2, response = $3, previous_sample_id = $4, summary_id = $5, account_id = $6, model_id = $7
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 243 (class 1255 OID 25893)
-- Name: update_summary(bigint, "text"); Type: FUNCTION; Schema: fine-tunning; Owner: postgres
--

CREATE FUNCTION "fine-tunning"."update_summary"("id" bigint, "summary" "text") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE "fine-tunning".summary
        SET summary = $2
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 252 (class 1255 OID 27571)
-- Name: delete_model(bigint); Type: FUNCTION; Schema: model; Owner: postgres
--

CREATE FUNCTION "model"."delete_model"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM model.model
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 255 (class 1255 OID 27574)
-- Name: delete_training(bigint); Type: FUNCTION; Schema: model; Owner: postgres
--

CREATE FUNCTION "model"."delete_training"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM model.training
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 250 (class 1255 OID 27569)
-- Name: insert_model("text", "text", integer, "date"); Type: FUNCTION; Schema: model; Owner: postgres
--

CREATE FUNCTION "model"."insert_model"("model" "text", "description" "text", "max_request" integer, "training_data_up_to" "date") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO model.model (model, description, max_request, training_data_up_to)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
    $_$;


--
-- TOC entry 253 (class 1255 OID 27572)
-- Name: insert_training("jsonb", bigint); Type: FUNCTION; Schema: model; Owner: postgres
--

CREATE FUNCTION "model"."insert_training"("data" "jsonb", "model_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO model.training (data, model_id)
        VALUES ($1, $2)
        RETURNING id;
    $_$;


--
-- TOC entry 251 (class 1255 OID 27570)
-- Name: update_model(bigint, "text", "text", integer, "date"); Type: FUNCTION; Schema: model; Owner: postgres
--

CREATE FUNCTION "model"."update_model"("id" bigint, "model" "text", "description" "text", "max_request" integer, "training_data_up_to" "date") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE model.model
        SET model = $2, description = $3, max_request = $4, training_data_up_to = $5
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 254 (class 1255 OID 27573)
-- Name: update_training(bigint, "jsonb", bigint); Type: FUNCTION; Schema: model; Owner: postgres
--

CREATE FUNCTION "model"."update_training"("id" bigint, "data" "jsonb", "model_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE model.training
        SET data = $2, model_id = $3
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 239 (class 1255 OID 25891)
-- Name: delete_account(bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."delete_account"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM "user".account
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 235 (class 1255 OID 25888)
-- Name: delete_platform(bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."delete_platform"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM "user".platform
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 248 (class 1255 OID 27206)
-- Name: delete_user(bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."delete_user"("id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        DELETE FROM "user"."user"
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 249 (class 1255 OID 27568)
-- Name: delete_user_account(bigint, bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."delete_user_account"("user_id" bigint, "account_id" bigint) RETURNS "record"
    LANGUAGE "sql"
    AS $_$
        DELETE FROM "user".user_account
        WHERE user_id = $1 AND account_id = $2
        RETURNING user_id, account_id;
    $_$;


--
-- TOC entry 237 (class 1255 OID 25889)
-- Name: insert_account("text", bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."insert_account"("name" "text", "platform_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO "user".account (name, platform_id)
        VALUES ($1, $2)
        RETURNING id;
    $_$;


--
-- TOC entry 241 (class 1255 OID 25886)
-- Name: insert_platform("text", "text"); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."insert_platform"("name" "text", "description" "text") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO "user".platform (name, description)
        VALUES ($1, $2)
        RETURNING id;
    $_$;


--
-- TOC entry 246 (class 1255 OID 27204)
-- Name: insert_user("text", "text"); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."insert_user"("name" "text", "email" "text") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        INSERT INTO "user"."user" (name, email)
        VALUES ($1, $2)
        RETURNING id;
    $_$;


--
-- TOC entry 236 (class 1255 OID 34081)
-- Name: insert_user_account(bigint, bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."insert_user_account"("user_id" bigint, "account_id" bigint) RETURNS "record"
    LANGUAGE "sql"
    AS $_$
        INSERT INTO "user".user_account (user_id, account_id)
        VALUES ($1, $2)
        RETURNING user_id, account_id;
    $_$;


--
-- TOC entry 238 (class 1255 OID 25890)
-- Name: update_account(bigint, "text", bigint); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."update_account"("id" bigint, "name" "text", "platform_id" bigint) RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE "user".account
        SET name = $2, platform_id = $3
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 242 (class 1255 OID 25887)
-- Name: update_platform(bigint, "text", "text"); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."update_platform"("id" bigint, "name" "text", "description" "text") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE "user".platform
        SET name = $2, description = $3
        WHERE id = $1
        RETURNING id;
    $_$;


--
-- TOC entry 247 (class 1255 OID 27205)
-- Name: update_user(bigint, "text", "text"); Type: FUNCTION; Schema: user; Owner: postgres
--

CREATE FUNCTION "user"."update_user"("id" bigint, "name" "text", "email" "text") RETURNS bigint
    LANGUAGE "sql"
    AS $_$
        UPDATE "user"."user"
        SET name = $2, email = $3
        WHERE id = $1
        RETURNING id;
    $_$;


SET default_tablespace = '';

SET default_table_access_method = "heap";

--
-- TOC entry 223 (class 1259 OID 34225)
-- Name: completion; Type: TABLE; Schema: completion; Owner: postgres
--

CREATE TABLE "completion"."completion" (
    "id" bigint NOT NULL,
    "prompt" "jsonb" DEFAULT '["<|endoftext|>"]'::"jsonb",
    "suffix" "text",
    "max_tokens" integer DEFAULT 16,
    "temperature" numeric DEFAULT 1,
    "top_p" numeric DEFAULT 1,
    "n" integer DEFAULT 1,
    "stream" boolean DEFAULT false,
    "logprobs" integer,
    "echo" boolean DEFAULT false,
    "stop" "jsonb",
    "presence_penalty" numeric DEFAULT 0,
    "frequency_penalty" numeric DEFAULT 0,
    "best_of" integer DEFAULT 1,
    "logit_bias" "jsonb",
    "model_id" bigint NOT NULL,
    "user_id" bigint NOT NULL
);


--
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE "completion"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON TABLE "completion"."completion" IS 'Given a prompt, the model will return one or more predicted completions, and can also return the probabilities of alternative tokens at each position.

This table stores completions and it''s attributes.';


--
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."prompt"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."prompt" IS 'string or array
Optional
Defaults to <|endoftext|>
The prompt(s) to generate completions for, encoded as a string, array of strings, array of tokens, or array of token arrays.

Note that <|endoftext|> is the document separator that the model sees during training, so if a prompt is not specified the model will generate as if from the beginning of a new document.';


--
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."suffix"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."suffix" IS 'string
Optional
Defaults to null
The suffix that comes after a completion of inserted text.';


--
-- TOC entry 3452 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."max_tokens"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."max_tokens" IS 'integer
Optional
Defaults to 16
The maximum number of tokens to generate in the completion.

The token count of your prompt plus max_tokens cannot exceed the model''s context length. Most models have a context length of 2048 tokens (except for the newest models, which support 4096).';


--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."temperature"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."temperature" IS 'number
Optional
Defaults to 1
What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or top_p but not both.';


--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."top_p"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."top_p" IS 'number
Optional
Defaults to 1
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.';


--
-- TOC entry 3455 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."n"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."n" IS 'integer
Optional
Defaults to 1
How many completions to generate for each prompt.

Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for max_tokens and stop.';


--
-- TOC entry 3456 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."stream"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."stream" IS 'boolean
Optional
Defaults to false
Whether to stream back partial progress. If set, tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.';


--
-- TOC entry 3457 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."logprobs"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."logprobs" IS 'integer
Optional
Defaults to null
Include the log probabilities on the logprobs most likely tokens, as well the chosen tokens. For example, if logprobs is 5, the API will return a list of the 5 most likely tokens. The API will always return the logprob of the sampled token, so there may be up to logprobs+1 elements in the response.

The maximum value for logprobs is 5. If you need more than this, please contact us through our Help center and describe your use case.';


--
-- TOC entry 3458 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."echo"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."echo" IS 'boolean
Optional
Defaults to false
Echo back the prompt in addition to the completion';


--
-- TOC entry 3459 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."stop"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."stop" IS 'string or array
Optional
Defaults to null
Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.';


--
-- TOC entry 3460 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."presence_penalty"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."presence_penalty" IS 'number
Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model''s likelihood to talk about new topics.

See more information about frequency and presence penalties.
https://platform.openai.com/docs/api-reference/parameter-details';


--
-- TOC entry 3461 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."frequency_penalty"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."frequency_penalty" IS 'number
Optional
Defaults to 0
Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model''s likelihood to repeat the same line verbatim.
See more information about frequency and presence penalties.
https://platform.openai.com/docs/api-reference/parameter-details';


--
-- TOC entry 3462 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."best_of"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."best_of" IS 'integer
Optional
Defaults to 1
Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token). Results cannot be streamed.

When used with n, best_of controls the number of candidate completions and n specifies how many to return – best_of must be greater than n.

Note: Because this parameter generates many completions, it can quickly consume your token quota. Use carefully and ensure that you have reasonable settings for max_tokens and stop.';


--
-- TOC entry 3463 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."logit_bias"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."logit_bias" IS 'map
Optional
Defaults to null
Modify the likelihood of specified tokens appearing in the completion.

Accepts a json object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated bias value from -100 to 100. You can use this tokenizer tool (which works for both GPT-2 and GPT-3) to convert text to token IDs. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.

As an example, you can pass {"50256": -100} to prevent the <|endoftext|> token from being generated.

The json and jsonb data types accept almost identical sets of values as input. The major practical difference is one of efficiency. The json data type stores an exact copy of the input text, which processing functions must reparse on each execution; while jsonb data is stored in a decomposed binary format that makes it slightly slower to input due to added conversion overhead, but significantly faster to process, since no reparsing is needed. jsonb also supports indexing, which can be a significant advantage.

https://www.postgresql.org/docs/current/datatype-json.html';


--
-- TOC entry 3464 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."model_id"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."model_id" IS 'Links to string
Required
ID of the model to use. You can use the List models API to see all of your available models, or see our Model overview for descriptions of them.';


--
-- TOC entry 3465 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN "completion"."user_id"; Type: COMMENT; Schema: completion; Owner: postgres
--

COMMENT ON COLUMN "completion"."completion"."user_id" IS 'Links to string
Required
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.';


--
-- TOC entry 222 (class 1259 OID 34224)
-- Name: completion_id_seq; Type: SEQUENCE; Schema: completion; Owner: postgres
--

CREATE SEQUENCE "completion"."completion_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3466 (class 0 OID 0)
-- Dependencies: 222
-- Name: completion_id_seq; Type: SEQUENCE OWNED BY; Schema: completion; Owner: postgres
--

ALTER SEQUENCE "completion"."completion_id_seq" OWNED BY "completion"."completion"."id";


--
-- TOC entry 232 (class 1259 OID 34279)
-- Name: sample; Type: TABLE; Schema: fine-tunning; Owner: postgres
--

CREATE TABLE "fine-tunning"."sample" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'UTC'::"text") NOT NULL,
    "prompt" "text",
    "response" "text",
    "previous_sample_id" bigint,
    "summary_id" bigint,
    "account_id" bigint NOT NULL,
    "model_id" bigint NOT NULL
);


--
-- TOC entry 3467 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE "sample"; Type: COMMENT; Schema: fine-tunning; Owner: postgres
--

COMMENT ON TABLE "fine-tunning"."sample" IS 'A chatbot will normally contain relevant context about the conversation ( psychological profile), summary of the conversation so far as well as most recent messages. For this use case the same past conversation can generate multiple rows in the dataset, each time with a slightly different context, for every agent generation as a completion. This use case will require a few thousand examples, as it will likely deal with different types of requests, and user issues. To ensure the performance is of high quality we recommend vetting the conversation samples to ensure the quality of agent messages. The summary can be generated with a separate text transformation fine tuned model. The dataset could look as follows:

{"prompt":"Summary: <summary of the interaction so far>\n\nSpecific information:<for example order details in natural language>\n\n###\n\nUser: <message1>\nWaifu: <response1>\nUser: <message2>\nWaifu:", "completion":" <response2>\n"}
{"prompt":"Summary: <summary of the interaction so far>\n\nSpecific information:<for example order details in natural language>\n\n###\n\nUser: <message1>\nWaifu: <response1>\nUser: <message2>\nWaifu: <response2>\nCustomer: <message3>\nWaifu:", "completion":" <response3>\n"}';


--
-- TOC entry 3468 (class 0 OID 0)
-- Dependencies: 232
-- Name: COLUMN "sample"."model_id"; Type: COMMENT; Schema: fine-tunning; Owner: postgres
--

COMMENT ON COLUMN "fine-tunning"."sample"."model_id" IS 'bigint
required
Agent is an instance of a model or a fine-tuned model that is answering this chat.';


--
-- TOC entry 231 (class 1259 OID 34278)
-- Name: sample_id_seq; Type: SEQUENCE; Schema: fine-tunning; Owner: postgres
--

CREATE SEQUENCE "fine-tunning"."sample_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3469 (class 0 OID 0)
-- Dependencies: 231
-- Name: sample_id_seq; Type: SEQUENCE OWNED BY; Schema: fine-tunning; Owner: postgres
--

ALTER SEQUENCE "fine-tunning"."sample_id_seq" OWNED BY "fine-tunning"."sample"."id";


--
-- TOC entry 234 (class 1259 OID 34289)
-- Name: summary; Type: TABLE; Schema: fine-tunning; Owner: postgres
--

CREATE TABLE "fine-tunning"."summary" (
    "id" bigint NOT NULL,
    "summary" "text",
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'UTC'::"text") NOT NULL
);


--
-- TOC entry 3470 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE "summary"; Type: COMMENT; Schema: fine-tunning; Owner: postgres
--

COMMENT ON TABLE "fine-tunning"."summary" IS 'Collects summary text from a chatlog.';


--
-- TOC entry 233 (class 1259 OID 34288)
-- Name: summary_id_seq; Type: SEQUENCE; Schema: fine-tunning; Owner: postgres
--

CREATE SEQUENCE "fine-tunning"."summary_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3471 (class 0 OID 0)
-- Dependencies: 233
-- Name: summary_id_seq; Type: SEQUENCE OWNED BY; Schema: fine-tunning; Owner: postgres
--

ALTER SEQUENCE "fine-tunning"."summary_id_seq" OWNED BY "fine-tunning"."summary"."id";


--
-- TOC entry 221 (class 1259 OID 34216)
-- Name: model; Type: TABLE; Schema: model; Owner: postgres
--

CREATE TABLE "model"."model" (
    "id" bigint NOT NULL,
    "model" "text" NOT NULL,
    "description" "text",
    "max_request" integer NOT NULL,
    "training_data_up_to" "date" NOT NULL
);


--
-- TOC entry 3472 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE "model"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON TABLE "model"."model" IS 'List and describe the various models available in the API. You can refer to the Models documentation to understand what models are available and the differences between them.';


--
-- TOC entry 3473 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN "model"."model"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON COLUMN "model"."model"."model" IS 'string
Required
A unique identifier representing the actual model name.';


--
-- TOC entry 3474 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN "model"."description"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON COLUMN "model"."model"."description" IS 'string
Optional
Description of the model.';


--
-- TOC entry 3475 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN "model"."max_request"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON COLUMN "model"."model"."max_request" IS 'integer
Required
Maximun amount of tokens to be used per request for the model in question.
When creating requets, the prompt and response tokens are added up, and need to be equal or lesser than this amount.';


--
-- TOC entry 3476 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN "model"."training_data_up_to"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON COLUMN "model"."model"."training_data_up_to" IS 'date
Required
Last date when the training data is up to in UTC.';


--
-- TOC entry 220 (class 1259 OID 34215)
-- Name: model_id_seq; Type: SEQUENCE; Schema: model; Owner: postgres
--

CREATE SEQUENCE "model"."model_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3477 (class 0 OID 0)
-- Dependencies: 220
-- Name: model_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: postgres
--

ALTER SEQUENCE "model"."model_id_seq" OWNED BY "model"."model"."id";


--
-- TOC entry 230 (class 1259 OID 34269)
-- Name: training; Type: TABLE; Schema: model; Owner: postgres
--

CREATE TABLE "model"."training" (
    "id" bigint NOT NULL,
    "data" "jsonb",
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'UTC'::"text") NOT NULL,
    "model_id" bigint
);


--
-- TOC entry 3478 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE "training"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON TABLE "model"."training" IS 'Training data is how you teach GPT-3 what you''d like it to say.

Your data must be a JSONL document, where each line is a prompt-completion pair corresponding to a training example. You can use our CLI data preparation tool to easily convert your data into this file format.';


--
-- TOC entry 3479 (class 0 OID 0)
-- Dependencies: 230
-- Name: COLUMN "training"."data"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON COLUMN "model"."training"."data" IS 'jasonb
Optional
In PostgreSQL, each of these entries should be stored as JSONB data types.
Examples:

{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
...

In PostgreSQL:

training_data = ''{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}
{"prompt": "<prompt text>", "completion": "<ideal generated text>"}''::jsonb';


--
-- TOC entry 3480 (class 0 OID 0)
-- Dependencies: 230
-- Name: COLUMN "training"."model_id"; Type: COMMENT; Schema: model; Owner: postgres
--

COMMENT ON COLUMN "model"."training"."model_id" IS 'bigint
Required
This is a reference to the model that this training data belongs to.';


--
-- TOC entry 229 (class 1259 OID 34268)
-- Name: training_id_seq; Type: SEQUENCE; Schema: model; Owner: postgres
--

CREATE SEQUENCE "model"."training_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3481 (class 0 OID 0)
-- Dependencies: 229
-- Name: training_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: postgres
--

ALTER SEQUENCE "model"."training_id_seq" OWNED BY "model"."training"."id";


--
-- TOC entry 227 (class 1259 OID 34253)
-- Name: account; Type: TABLE; Schema: user; Owner: postgres
--

CREATE TABLE "user"."account" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "platform_id" bigint NOT NULL
);


--
-- TOC entry 3482 (class 0 OID 0)
-- Dependencies: 227
-- Name: TABLE "account"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON TABLE "user"."account" IS 'User catalog, used to identify who is making the requests.';


--
-- TOC entry 3483 (class 0 OID 0)
-- Dependencies: 227
-- Name: COLUMN "account"."name"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON COLUMN "user"."account"."name" IS 'string
Required
A unique identifier representing your end-user account on a given platform, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';


--
-- TOC entry 226 (class 1259 OID 34252)
-- Name: account_id_seq; Type: SEQUENCE; Schema: user; Owner: postgres
--

CREATE SEQUENCE "user"."account_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3484 (class 0 OID 0)
-- Dependencies: 226
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: user; Owner: postgres
--

ALTER SEQUENCE "user"."account_id_seq" OWNED BY "user"."account"."id";


--
-- TOC entry 225 (class 1259 OID 34244)
-- Name: platform; Type: TABLE; Schema: user; Owner: postgres
--

CREATE TABLE "user"."platform" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "description" "text"
);


--
-- TOC entry 3485 (class 0 OID 0)
-- Dependencies: 225
-- Name: TABLE "platform"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON TABLE "user"."platform" IS 'Platform information, where the user is interacting with the AI.
The same user may create several accounts on the same or different platforms.';


--
-- TOC entry 3486 (class 0 OID 0)
-- Dependencies: 225
-- Name: COLUMN "platform"."name"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON COLUMN "user"."platform"."name" IS 'text
Required
Name of the platform.';


--
-- TOC entry 3487 (class 0 OID 0)
-- Dependencies: 225
-- Name: COLUMN "platform"."description"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON COLUMN "user"."platform"."description" IS 'text
Optional
Description of the platform.';


--
-- TOC entry 224 (class 1259 OID 34243)
-- Name: platform_id_seq; Type: SEQUENCE; Schema: user; Owner: postgres
--

CREATE SEQUENCE "user"."platform_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3488 (class 0 OID 0)
-- Dependencies: 224
-- Name: platform_id_seq; Type: SEQUENCE OWNED BY; Schema: user; Owner: postgres
--

ALTER SEQUENCE "user"."platform_id_seq" OWNED BY "user"."platform"."id";


--
-- TOC entry 219 (class 1259 OID 34204)
-- Name: user; Type: TABLE; Schema: user; Owner: postgres
--

CREATE TABLE "user"."user" (
    "id" bigint NOT NULL,
    "name" "text" NOT NULL,
    "email" "text" NOT NULL,
    "created_at" timestamp with time zone DEFAULT ("now"() AT TIME ZONE 'UTC'::"text") NOT NULL
);


--
-- TOC entry 3489 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE "user"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON TABLE "user"."user" IS 'User catalog, used to identify the human who is making the requests.';


--
-- TOC entry 3490 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN "user"."name"; Type: COMMENT; Schema: user; Owner: postgres
--

COMMENT ON COLUMN "user"."user"."name" IS 'string
Required
A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.
Learn more.
https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids';


--
-- TOC entry 228 (class 1259 OID 34263)
-- Name: user_account; Type: TABLE; Schema: user; Owner: postgres
--

CREATE TABLE "user"."user_account" (
    "user_id" bigint NOT NULL,
    "account_id" bigint NOT NULL
);


--
-- TOC entry 218 (class 1259 OID 34203)
-- Name: user_id_seq; Type: SEQUENCE; Schema: user; Owner: postgres
--

CREATE SEQUENCE "user"."user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3491 (class 0 OID 0)
-- Dependencies: 218
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: user; Owner: postgres
--

ALTER SEQUENCE "user"."user_id_seq" OWNED BY "user"."user"."id";


--
-- TOC entry 3245 (class 2604 OID 34228)
-- Name: completion id; Type: DEFAULT; Schema: completion; Owner: postgres
--

ALTER TABLE ONLY "completion"."completion" ALTER COLUMN "id" SET DEFAULT "nextval"('"completion"."completion_id_seq"'::"regclass");


--
-- TOC entry 3260 (class 2604 OID 34282)
-- Name: sample id; Type: DEFAULT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."sample" ALTER COLUMN "id" SET DEFAULT "nextval"('"fine-tunning"."sample_id_seq"'::"regclass");


--
-- TOC entry 3262 (class 2604 OID 34292)
-- Name: summary id; Type: DEFAULT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."summary" ALTER COLUMN "id" SET DEFAULT "nextval"('"fine-tunning"."summary_id_seq"'::"regclass");


--
-- TOC entry 3244 (class 2604 OID 34219)
-- Name: model id; Type: DEFAULT; Schema: model; Owner: postgres
--

ALTER TABLE ONLY "model"."model" ALTER COLUMN "id" SET DEFAULT "nextval"('"model"."model_id_seq"'::"regclass");


--
-- TOC entry 3258 (class 2604 OID 34272)
-- Name: training id; Type: DEFAULT; Schema: model; Owner: postgres
--

ALTER TABLE ONLY "model"."training" ALTER COLUMN "id" SET DEFAULT "nextval"('"model"."training_id_seq"'::"regclass");


--
-- TOC entry 3257 (class 2604 OID 34256)
-- Name: account id; Type: DEFAULT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."account" ALTER COLUMN "id" SET DEFAULT "nextval"('"user"."account_id_seq"'::"regclass");


--
-- TOC entry 3256 (class 2604 OID 34247)
-- Name: platform id; Type: DEFAULT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."platform" ALTER COLUMN "id" SET DEFAULT "nextval"('"user"."platform_id_seq"'::"regclass");


--
-- TOC entry 3242 (class 2604 OID 34207)
-- Name: user id; Type: DEFAULT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."user" ALTER COLUMN "id" SET DEFAULT "nextval"('"user"."user_id_seq"'::"regclass");


--
-- TOC entry 3271 (class 2606 OID 34242)
-- Name: completion completion_pkey; Type: CONSTRAINT; Schema: completion; Owner: postgres
--

ALTER TABLE ONLY "completion"."completion"
    ADD CONSTRAINT "completion_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3283 (class 2606 OID 34287)
-- Name: sample sample_pkey; Type: CONSTRAINT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."sample"
    ADD CONSTRAINT "sample_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3285 (class 2606 OID 34297)
-- Name: summary summary_pkey; Type: CONSTRAINT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."summary"
    ADD CONSTRAINT "summary_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3269 (class 2606 OID 34223)
-- Name: model model_pkey; Type: CONSTRAINT; Schema: model; Owner: postgres
--

ALTER TABLE ONLY "model"."model"
    ADD CONSTRAINT "model_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3281 (class 2606 OID 34277)
-- Name: training training_pkey; Type: CONSTRAINT; Schema: model; Owner: postgres
--

ALTER TABLE ONLY "model"."training"
    ADD CONSTRAINT "training_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3275 (class 2606 OID 34262)
-- Name: account account_name_platform_id_key; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."account"
    ADD CONSTRAINT "account_name_platform_id_key" UNIQUE ("name", "platform_id");


--
-- TOC entry 3277 (class 2606 OID 34260)
-- Name: account account_pkey; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."account"
    ADD CONSTRAINT "account_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3273 (class 2606 OID 34251)
-- Name: platform platform_pkey; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."platform"
    ADD CONSTRAINT "platform_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3279 (class 2606 OID 34267)
-- Name: user_account user_account_pkey; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."user_account"
    ADD CONSTRAINT "user_account_pkey" PRIMARY KEY ("user_id", "account_id");


--
-- TOC entry 3265 (class 2606 OID 34214)
-- Name: user user_name_email_key; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."user"
    ADD CONSTRAINT "user_name_email_key" UNIQUE ("name", "email");


--
-- TOC entry 3267 (class 2606 OID 34212)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."user"
    ADD CONSTRAINT "user_pkey" PRIMARY KEY ("id");


--
-- TOC entry 3286 (class 2606 OID 34298)
-- Name: completion completion_model_id_fkey; Type: FK CONSTRAINT; Schema: completion; Owner: postgres
--

ALTER TABLE ONLY "completion"."completion"
    ADD CONSTRAINT "completion_model_id_fkey" FOREIGN KEY ("model_id") REFERENCES "model"."model"("id") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3287 (class 2606 OID 34303)
-- Name: completion completion_user_id_fkey; Type: FK CONSTRAINT; Schema: completion; Owner: postgres
--

ALTER TABLE ONLY "completion"."completion"
    ADD CONSTRAINT "completion_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user"."user"("id") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3292 (class 2606 OID 34333)
-- Name: sample sample_account_id_fkey; Type: FK CONSTRAINT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."sample"
    ADD CONSTRAINT "sample_account_id_fkey" FOREIGN KEY ("account_id") REFERENCES "user"."account"("id") ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- TOC entry 3293 (class 2606 OID 34343)
-- Name: sample sample_model_id_fkey; Type: FK CONSTRAINT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."sample"
    ADD CONSTRAINT "sample_model_id_fkey" FOREIGN KEY ("model_id") REFERENCES "model"."model"("id") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3294 (class 2606 OID 34338)
-- Name: sample sample_previous_sample_id_fkey; Type: FK CONSTRAINT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."sample"
    ADD CONSTRAINT "sample_previous_sample_id_fkey" FOREIGN KEY ("previous_sample_id") REFERENCES "fine-tunning"."sample"("id") ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- TOC entry 3295 (class 2606 OID 34328)
-- Name: sample sample_summary_id_fkey; Type: FK CONSTRAINT; Schema: fine-tunning; Owner: postgres
--

ALTER TABLE ONLY "fine-tunning"."sample"
    ADD CONSTRAINT "sample_summary_id_fkey" FOREIGN KEY ("summary_id") REFERENCES "fine-tunning"."summary"("id") ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- TOC entry 3291 (class 2606 OID 34323)
-- Name: training training_model_id_fkey; Type: FK CONSTRAINT; Schema: model; Owner: postgres
--

ALTER TABLE ONLY "model"."training"
    ADD CONSTRAINT "training_model_id_fkey" FOREIGN KEY ("model_id") REFERENCES "model"."model"("id") ON UPDATE CASCADE ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 3288 (class 2606 OID 34308)
-- Name: account account_platform_id_fkey; Type: FK CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."account"
    ADD CONSTRAINT "account_platform_id_fkey" FOREIGN KEY ("platform_id") REFERENCES "user"."platform"("id") ON UPDATE CASCADE ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 3289 (class 2606 OID 34318)
-- Name: user_account user_account_account_id_fkey; Type: FK CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."user_account"
    ADD CONSTRAINT "user_account_account_id_fkey" FOREIGN KEY ("account_id") REFERENCES "user"."account"("id") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3290 (class 2606 OID 34313)
-- Name: user_account user_account_user_id_fkey; Type: FK CONSTRAINT; Schema: user; Owner: postgres
--

ALTER TABLE ONLY "user"."user_account"
    ADD CONSTRAINT "user_account_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user"."user"("id") ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


-- Completed on 2023-02-15 12:37:11

--
-- PostgreSQL database dump complete
--

