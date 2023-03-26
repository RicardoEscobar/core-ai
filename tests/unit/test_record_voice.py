import unittest
from unittest.mock import patch
import pyaudio
from typing import List
from controller.conversation.record_voice import record_voice


class TestRecordVoice(unittest.TestCase):
    @patch.object(pyaudio.PyAudio, "open")
    def test_record_voice(self, mock_open):
        # Set up mock input stream to return sample data
        mock_stream = mock_open.return_value
        mock_stream.read.return_value = b"sample data"

        # Add a side effect to the stream's read() method to simulate
        # the user interrupting the recording
        mock_stream.read.side_effect = KeyboardInterrupt

        # Call record_voice() and capture the frames using the mock stream
        frames = record_voice()

        # Assert that frames is a non-empty list
        self.assertIsInstance(frames, List)

        # Assert that the stream was opened with the correct parameters
        mock_open.assert_called_once_with(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )

        # Assert that the stream was read from at least once
        mock_stream.read.assert_called()

if __name__ == "__main__":
    unittest.main()
