"""This module contains the unit tests for the conversation_handler module."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    if str(project_directory) not in sys.path:
        sys.path.append(str(project_directory))

import unittest
import logging

from controller.conversation_handler import truncate_conversation_persona
from controller.create_logger import create_logger

# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_conversation_handler",
    logger_filename="test_conversation_handler.log",
    log_directory="logs/tests",
    console_logging=False,
    console_log_level=logging.INFO,
)


class TestConversationHandler(unittest.TestCase):
    """This is the unit test class for the ConversationHandler class."""

    @classmethod
    def setUpClass(cls):
        """Set up the ConversationHandler class unit test."""
        # Create class logger instance
        cls.logger = module_logger
        cls.logger.info("===Testing ConversationHandler class===")

    def test_truncate_conversation_persona(self):
        """Test that the truncate_conversation_persona function truncates the conversation correctly."""
        persona = {
            "messages": [
                {"role": "system", "content": "You are an AI asistant."},
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "How are you?"},
                {"role": "user", "content": "I'm fine"},
                {"role": "assistant", "content": "Goodbye"},
                {"role": "system", "content": "Goodbye"},
            ]
        }
        expected_persona = {
            # Most recent messages are kept.
            "messages": [
                {"role": "user", "content": "I'm fine"},
                {"role": "assistant", "content": "Goodbye"},
                {"role": "system", "content": "Goodbye"},
            ],
            # Older messages are moved to "old_messages".
            "old_messages": [
                {"role": "system", "content": "You are an AI asistant."},
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "How are you?"},
            ],
        }

        # Assert that if persona["messages"] is not empty, then persona["old_messages"] is not empty.

        # Truncate the conversation.
        actual_persona = truncate_conversation_persona(persona)

        # Check that the conversation was truncated correctly.
        self.assertEqual(actual_persona, expected_persona)

        # Assert that if persona["messages"] is empty, then persona["old_messages"] is empty.
        persona = {"messages": []}
        expected_persona = {"messages": [], "old_messages": []}

        # Truncate the conversation.
        actual_persona = truncate_conversation_persona(persona)

        # Check that the conversation was truncated correctly.
        self.assertEqual(actual_persona, expected_persona)


        # Assert that if persona["messages"] does not exist, raise a KeyError.
        persona = {}
        expected_persona = {}

        # Check that the conversation was truncated correctly.
        with self.assertRaises(KeyError):
            actual_persona = truncate_conversation_persona(persona)

        self.logger.info("✅ test_truncate_conversation_persona passed.")


if __name__ == "__main__":
    unittest.main()
