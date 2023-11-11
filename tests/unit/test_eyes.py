"""This is the unit test class for the controller.vision.eyes module."""
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

from controller.vision.eyes import Eyes
from controller.create_logger import create_logger

# Create a logger instance
log = create_logger(
    logger_name="tests.unit.test_eyes",
    logger_filename="test_eyes.log",
    log_directory="logs/tests",
    console_logging=True,
    console_log_level=logging.INFO,
)

class TestEyes(unittest.TestCase):
    """This is the unit test class for the controller.vision.eyes module."""

    def test_eyes(self):
        """Test that the eyes class can be instantiated."""

        log.info("===Testing eyes class===")
        # Create an instance of the eyes class
        eyes = Eyes()

        # Verify that the eyes class was instantiated
        self.assertIsInstance(eyes, Eyes)
        log.debug("✅ The eyes class was instantiated.")

if __name__ == "__main__":
    unittest.main()