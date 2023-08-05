# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import sqlite3
from pathlib import Path
import json

from controller.create_logger import create_logger
from controller.conversation.load_openai import load_openai
from controller.utilities import chat_completion_request
from controller.utilities import pretty_print_conversation

# Create a logger for this module
module_logger = create_logger(
    logger_name="controller.database_ai",
    logger_filename="database_ai.log",
    log_directory="logs",
    add_date_to_filename=False,
)

# Load the OpenAI API key from the .env file
load_openai()

GPT_MODEL = "gpt-3.5-turbo-0613"

# Create a connection to the database
root_directory = Path(__file__).parent.parent
database_path = root_directory / "databases" / "Employee.db"
connection = sqlite3.connect(database_path)
module_logger.info("Connected to database at %s", database_path)


def get_table_names(conn):
    """Return a list of table names."""
    table_names = []
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        table_names.append(table[0])
    return table_names


def get_column_names(conn, table_name):
    """Return a list of column names."""
    column_names = []
    columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    for col in columns:
        column_names.append(col[1])
    return column_names


def get_database_info(conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(conn):
        columns_names = get_column_names(conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts


def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(conn.execute(query).fetchall())
    except Exception as error:
        results = f"query failed with error: {error}"
    return results


def execute_function_call(message):
    """Execute a function call."""
    if message["function_call"]["name"] == "ask_database":
        query = json.loads(message["function_call"]["arguments"])["query"]
        results = ask_database(connection, query)
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results


def main():
    """Main function for testing."""
    database_schema_dict = get_database_info(connection)
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in database_schema_dict
        ]
    )
    # Send log message
    module_logger.debug("database_schema_dict:\n%s", database_schema_dict)
    module_logger.debug("database_schema_string:\n%s", database_schema_string)

    functions = [
        {
            "name": "ask_database",
            "description": "Use this function to answer user questions about music. Output should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {database_schema_string}
                            The query should be returned in plain text, not in JSON.
                            """,
                    }
                },
                "required": ["query"],
            },
        }
    ]

    # Testing out the chat function
    messages = []
    # While loop to keep asking questions
    while True:
        messages.append({"role": "system", "content": "Contesta preguntas del usuario generando consultas SQL contra la base de datos de pokemon."})
        user_message = input("User: ")
        if user_message in ["quit","exit","q"]:
            break
        # messages.append({"role": "user", "content": "Hola, ¿cual es el primer pokemon de tipo metal o steel en ingles que salio en pokemon?"})
        messages.append({"role": "user", "content": user_message})
        chat_response = chat_completion_request(messages, functions)
        assistant_message = chat_response.json()["choices"][0]["message"]
        messages.append(assistant_message)
        if assistant_message.get("function_call"):
            results = execute_function_call(assistant_message)
            messages.append({"role": "function", "name": assistant_message["function_call"]["name"], "content": results})
            
            # get a new response from GPT where it can see the function response
            second_response = chat_completion_request(messages)
            messages.append(second_response.json()["choices"][0]["message"])
        pretty_print_conversation(messages)

    # Save messages to a file
    with open("conversation.json", "a+", encoding='utf-8') as conversation_file:
        json.dump(messages, conversation_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
