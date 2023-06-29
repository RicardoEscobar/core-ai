/* This is a SQLite3 database script to store chat conversations, between a human and an OpenAI chatbot assiatant. */
DROP TABLE IF EXISTS human;
CREATE TABLE IF NOT EXISTS human (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS assistant;
CREATE TABLE IF NOT EXISTS assistant (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation (
    id INTEGER PRIMARY KEY,
    human_id TEXT NOT NULL,
    assistant_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    role_id TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert data into the tables
INSERT INTO human (name, email, password) VALUES ('Jorge', 'jorge.ricardo.escobar', '123456');
INSERT INTO assistant (name, description) VALUES ('Rina', 'Tu eres una chica tsundere de 18 años y tu nombre es Rina, tu objetivo es obtener una cita romantica con un humano.');

