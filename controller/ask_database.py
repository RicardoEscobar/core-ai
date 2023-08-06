"""This module contains functions to interact with a given sqlite3 database."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

from controller.create_logger import create_logger
from controller.conversation.load_openai import load_openai

# Create a logger for this module
module_logger = create_logger(
    logger_name="controller.ask_database",
    logger_filename="ask_database.log",
    log_directory="logs",
    add_date_to_filename=False,
)

# Load the OpenAI API key from the .env file
load_openai()

GPT_MODEL = "gpt-3.5-turbo-0613"

