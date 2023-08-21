# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    if str(project_directory) not in sys.path:
        sys.path.append(str(project_directory))

import os
import unittest
from unittest.mock import patch, MagicMock
import logging
import asyncio

from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand

from controller.vtuber_chat import VTuberChat
from controller.create_logger import create_logger


# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_vtuber_chat",
    logger_filename="test_vtuber_chat.log",
    log_directory="logs/tests",
    console_logging=False,
    console_log_level=logging.INFO,
)


class TestVTuberChat(unittest.TestCase):

    logger = module_logger

    def __init__(self, *args, **kwargs):
        super(TestVTuberChat, self).__init__(*args, **kwargs)
        self.logger.info("===Testing VTuberChat class===")

    def setUp(self):
        """Set up the VTuberChat class unit test."""
        self.logger.info("Setting up VTuberChat class unit test.")
        self.chat = VTuberChat()
        self.chat.user_scope = "testuser"
        self.chat.target_channels = ["testroom1", "testroom2"]

    def test_init(self):
        """Test the VTuberChat class initialization"""
        self.assertIsNotNone(self.chat)
        self.assertIsNotNone(self.chat.user_scope)

    def test_save_log(self):
        """Test the save_log function"""
        self.logger.info("Testing save_log function.")
        with self.assertRaises(TypeError):
            self.chat.save_log(msg="Test message")

        # Create a mock ChatMessage object
        mock_message = MagicMock(spec=ChatMessage)
        mock_message.user.name = "testuser"
        mock_message.text = "Hello, world!"
        mock_message.room.name = "testroom"

        # Call the save_log method with the mock message
        self.chat.save_log(mock_message)

        # Check that the log file was created and contains the expected message
        log_file_path = f"chat/{mock_message.room.name}.md"
        self.assertTrue(os.path.exists(log_file_path))
        with open(log_file_path, "r", encoding="utf-8") as log_file:
            log_contents = log_file.read()
            self.assertIn(mock_message.text, log_contents)

        # Delete the log file
        os.remove(log_file_path)


if __name__ == "__main__":
    unittest.main()
