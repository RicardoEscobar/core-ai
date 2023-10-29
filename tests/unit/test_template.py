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

from controller.vtuber_chat import save_log, on_ready, on_message, on_sub, test_command, run
from controller.create_logger import create_logger


# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_twitch",
    logger_filename="test_twitch.log",
    log_directory="logs/tests",
    console_logging=True,
    console_log_level=logging.INFO,
)

class TestTwitch(unittest.TestCase):
    def test_init(self):
        pass


if __name__ == "__main__":
    unittest.main()