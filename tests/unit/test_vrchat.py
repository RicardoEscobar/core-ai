"""Unit tests for the VRChat module."""
if __name__ == "__main__":
    import sys
    import os

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.append(ROOT_DIR)

import unittest
from unittest.mock import patch
from pathlib import Path
import logging

from controller.vrchat import VRChat


class TestVRChat(unittest.TestCase):
    """Test the vrchat module."""

    # @patch("pythonosc.udp_client.SimpleUDPClient.send_message")
    def test_send_text(self):
        """Test the send_text method."""

        # Create VRChat object
        vrchat = VRChat()

        # Assert that last_sent_text is changed after sending text.
        vrchat.send_text("Hello World!")
        self.assertEqual(vrchat.last_sent_text, "Hello World!")

        # Assert that ValueError is raised when sending empty text.
        with self.assertRaises(ValueError):
            vrchat.send_text()

        # Assert that ValueError is raised when surpassing text limit.
        with self.assertRaises(ValueError):
            vrchat.send_text("a" * (vrchat.text_limit + 1))

if __name__ == "__main__":
    unittest.main()