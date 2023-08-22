"""Unit tests for stream_completion.py"""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    if str(project_directory) not in sys.path:
        sys.path.append(str(project_directory))

import unittest
from unittest.mock import patch, MagicMock
import logging

from controller.stream_completion import StreamCompletion
from controller.create_logger import create_logger


# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_stream_completion",
    logger_filename="stream_completion.log",
    log_directory="logs/tests",
    console_logging=False,
    console_log_level=logging.INFO,
)


class TestStreamCompletion(unittest.TestCase):
    """This is the unit test class for the StreamCompletion class."""

    @classmethod
    def setUpClass(cls):
        """Set up the StreamCompletion class unit test."""
        # Create class logger instance
        cls.logger = module_logger
        cls.logger.info("===Testing StreamCompletion class===")

    def setUp(self):
        """Set up the StreamCompletion class unit test."""
        self.stream_completion = StreamCompletion()

    def test_get_token_count(self):
        # Create a test string and model name
        test_string = "Hello, world!"
        model_name = "gpt2"

        # Call the get_token_count method
        num_tokens = StreamCompletion.get_token_count(test_string, model_name)

        # Verify that the number of tokens is correct
        self.assertEqual(num_tokens, 4)

        self.logger.debug("The string %s has %s tokens.", test_string, num_tokens)
        self.logger.info("Tested the get_token_count method.")


if __name__ == "__main__":
    unittest.main()