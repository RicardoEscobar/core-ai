"""This module controls the VRChat client."""
if __name__ == "__main__":
    import sys
    import os

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(ROOT_DIR)

import logging
from pathlib import Path

import time
from pythonosc.udp_client import SimpleUDPClient


class VRChat:
    """This class controls the VRChat client."""

    # Clas constants for VRChat connection
    IP = "127.0.0.1"
    PORT = 9000  # send data to VRChat client

    # Create client
    client = SimpleUDPClient(IP, PORT)

    def __init__(self):
        """The constructor for the VRChat class."""

        # Initialize logging from vrchat.py
        self.setup_logging()

        # VRChat limits the number of characters that can be sent to 144 per chat bubble.
        self.text_limit = 144
        self.last_sent_text = ""

    def send_text(self, text: str = ""):
        """This method sends the text to the VRChat client."""

        address = "/chatbox/input"
        # If self.text is not empty, send self.text to the VRChat client.
        if text != "":
            # VRChat limits the number of characters that can be sent to 144 per chat bubble.
            if len(text) > self.text_limit:
                self.logger.error(
                    "Text length %d exceeds text limit %d", len(text), self.text_limit
                )
                raise ValueError(
                    "Text length {} exceeds text limit {}".format(
                        len(text), self.text_limit
                    )
                )
            self.logger.debug("Sending text: %s", repr(text))
            self.client.send_message(address, text)
            self.last_sent_text = text
        else:
            self.logger.error("Text cannot be empty.")
            raise ValueError("Text cannot be empty.")

    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        LOG_FILE_NAME = Path(__file__).stem + ".log"
        ROOT_DIR = Path(__file__).resolve().parents[1]

        log_file_path = ROOT_DIR / "logs" / LOG_FILE_NAME
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        cls.file_handler = logging.FileHandler(log_file_path)
        cls.file_handler.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        cls.console_handler = logging.StreamHandler()
        cls.console_handler.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formater_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        cls.formatter = logging.Formatter(formater_str)
        cls.console_handler.setFormatter(cls.formatter)
        cls.file_handler.setFormatter(cls.formatter)

        # add the handlers to the logger
        cls.logger.addHandler(cls.console_handler)
        cls.logger.addHandler(cls.file_handler)
        cls.logger.debug("Logging configuration finished.")
