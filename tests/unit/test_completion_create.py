"""Unit tests for completion_create.py"""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import unittest
from unittest.mock import patch
from unittest.mock import mock_open

from controller.create_logger import create_logger
from controller.waifuai.completion_create import (
    generate_message,
    get_response,
    save_conversation,
)

# Create a logger for this module
module_logger = create_logger(
    logger_name="tests.unit.test_completion_create",
    logger_filename="test_completion_create.log",
    log_directory="logs/tests",
    add_date_to_filename=False,
)


class TestCompletitionCreate(unittest.TestCase):
    """Test case for completion_create.py"""

    @classmethod
    def setUpClass(cls):
        """Setup the test class"""
        cls.logger = module_logger

    def test_generate_message_system(self):
        """Test generate_message() for system, user, and assistant roles"""
        self.logger.debug(
            "=> Testing generate_message() for system, user, and assistant roles"
        )
        # Test system role
        message = generate_message("system", "Hello, world!")
        self.assertEqual(message["role"], "system")
        self.assertEqual(message["content"], "Hello, world!")
        self.logger.debug("Asserted system role message: %s", message)

        # Test user role
        message = generate_message("user", "How are you?")
        self.assertEqual(message["role"], "user")
        self.assertEqual(message["content"], "How are you?")
        self.logger.debug("Asserted user role message: %s", message)

        # Test assistant role
        message = generate_message("assistant", "I'm doing well, thank you!")
        self.assertEqual(message["role"], "assistant")
        self.assertEqual(message["content"], "I'm doing well, thank you!")
        self.logger.debug("Asserted assistant role message: %s", message)

    @patch("openai.ChatCompletion.create")
    def test_get_response(self, mock_completion_create):
        """Test get_response() function that gets the answer from the OpenAI API."""
        self.logger.debug(
            "=> Testing get_response() function that gets the answer from the OpenAI API."
        )

        # Mock the OpenAI API response
        mock_completion_create.return_value = {
            "choices": [
                {
                    "finish_reason": "length",
                    "index": 0,
                    "logprobs": None,
                    "message": {"role": "assistant", "content": "Hello, world!"},
                }
            ],
            "created": 1623523893,
            "id": "cmpl-2g5jv5Q8Zq4Z8W0q9k4J4uJL",
            "model": "davinci:2020-05-03",
            "object": "text_completion",
        }

        # Test get_response() function
        actual_response = get_response(
            messages=[
                {"role": "user", "content": "Hello!"},
                {"role": "system", "content": "How are you?"},
            ]
        )

        self.logger.debug("Actual response: %s", actual_response)
        expected_response = "Hello, world!"
        self.assertEqual(actual_response, expected_response)
        self.logger.debug("Asserted response: %s", actual_response)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_conversation(self, mock_file):
        """Test save_conversation() function that saves the conversation to a file."""

        self.logger.debug(
            "=> Testing save_conversation() function that saves the conversation to a file."
        )
        persona = {
            "conversation_file_path": "/path/to/conversation.py",
            "name": "John",
            "age": 30,
        }
        save_conversation(persona)
        self.logger.debug("Saved conversation: %s", persona)

        mock_file.assert_called_once_with(
            "/path/to/conversation.py", mode="w", encoding="utf-8"
        )
        self.logger.debug("Asserted file path: %s", "/path/to/conversation.py")

        expected_file_content = (
            '"""This is an example of a conversation that can be used by the podcaster_ai_controller.py script."""\n'
            f"from pathlib import Path, WindowsPath, PosixPath, PureWindowsPath, PurePosixPath, PurePath\n\n"
            f"# This dictionary is used to save the conversation to a file.\n"
            f"persona  = {repr(persona)}\n"
        )

        handle = mock_file()
        handle.write.assert_called_once_with(expected_file_content)

        # Assert that if the 'persona' argument is not a dictionary, then raise TypeError
        with self.assertRaises(TypeError):
            save_conversation("John")
        self.logger.debug("Asserted TypeError: %s", "John")


if __name__ == "__main__":
    unittest.main()
