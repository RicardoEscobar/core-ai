"""Unit tests for the chat module."""

# add the project root directory to the system path
if __name__ == '__main__':
    from pathlib import Path
    project_directory = Path(__file__).parent.parent
    print(project_directory)
    import sys
    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))
    print(sys.path)

import unittest
from unittest.mock import patch

from view.chat import send_text, send_command


class TestChat(unittest.TestCase):
    """Test the chat module."""

    @patch("view.chat.send_text")
    def test_send_text(self, mock_send_text):
        """Test the send_text function."""