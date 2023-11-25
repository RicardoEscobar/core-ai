"""This is the unit test class for the controller.get_token_count module."""
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

from controller.get_token_count import get_token_count
from controller.create_logger import create_logger

# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_get_token_count",
    logger_filename="get_token_count.log",
    log_directory="logs/tests",
    console_logging=True,
    console_log_level=logging.INFO,
)

class TestGetTokenCount(unittest.TestCase):
    """This is the unit test class for the get_token_count function."""

    def test_get_token_count(self):
        """Test that the get_token_count function returns the correct number of tokens."""

        module_logger.info("===Testing get_token_count function===")
        # Create a test string and model name
        test_string = "Hello, world!"
        model_name = "gpt2"

        # Call the get_token_count function
        num_tokens = get_token_count(test_string, model_name)

        # Verify that the number of tokens is correct
        self.assertEqual(num_tokens, 4)
        module_logger.debug("The string %s has %s tokens.", repr(test_string), num_tokens)

if __name__ == "__main__":
    unittest.main()