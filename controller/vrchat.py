"""This module controls the VRChat client."""
if __name__ == "__main__":
    import sys
    import os

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(ROOT_DIR)

from pathlib import Path
import textwrap
from typing import List
import threading

import time
from pythonosc.udp_client import SimpleUDPClient

from controller.create_logger import create_logger

# Create logger
module_logger = create_logger(
    logger_name=__name__,
    logger_filename="vrchat.log",
    log_directory="logs",
    add_date_to_filename=False,
)

class VRChat:
    """This class controls the VRChat client."""

    # Clas constants for VRChat connection
    IP = "127.0.0.1"
    PORT = 9000  # send data to VRChat client

    # VRChat limits the number of characters that can be sent to 144 per chat bubble.
    TEXT_LIMIT = 144

    # Create client
    client = SimpleUDPClient(IP, PORT)

    def __init__(self):
        """The constructor for the VRChat class."""

        self.last_sent_text = ""

        # Create logger
        self.logger = module_logger

        # Dictionary of emotes for the Runa avatar.
        # id: avtr_f0036585-e4fc-4b3e-b65d-02193fb3a86d
        # name: Runa
        # filepath: C:\Users\Jorge\AppData\LocalLow\VRChat\VRChat\OSC\usr_b7061573-c133-411b-a8c4-aa2ea519bb94\Avatars\avtr_f0036585-e4fc-4b3e-b65d-02193fb3a86d.json
        self.emote_dict = {
            "none": 0,
            "wave": 1,
            "applause": {"emote": 2, "duration": 5},  # loops, needs to be stopped
            "point": 3,
            "cheer": {"emote": 4, "duration": 5},  # loops, needs to be stopped
            "dance": 5,  # loops, needs to be stopped
            "backflip": 6,
            "sad": 7,
            "die": 8,  # loops, needs to be stopped
            "t-pose": 9,  # loops, needs to be stopped
            "hk-walk": {"emote": 10, "duration": 5},  # loops, needs to be stopped
            "dont-start-now": 11,  # loops, needs to be stopped
            "ashton-salt-lake": 12,  # loops, needs to be stopped
            "blinding-lights": 13,  # loops, needs to be stopped
            "skinwalker": 14,  # loops, needs to be stopped
            "laugh": {"emote": 15, "duration": 5},  # loops, needs to be stopped
            "moonwalking": 16,  # loops, needs to be stopped
            "armup": 17,  # loops, needs to be stopped
            "afrohouse": 18,  # loops, needs to be stopped
            "ashton-boardwalk": 19,  # loops, needs to be stopped
            "breakdance": 20,  # loops, needs to be stopped
            "a1-dance": {"emote": 21, "duration": 10},  # loops, needs to be stopped
            "bbd": 22,  # loops, needs to be stopped
            "balletspin": 23,  # loops, needs to be stopped
            "calculated": {"emote": 24, "duration": 3},  # loops, needs to be stopped
        }

    def send_vrc_emote(self, emote_key: str = "none"):
        """This method sends the emote to the VRChat client."""

        address = "/avatar/parameters/VRCEmote"
        # If emote_dict[emote_key] us a dictionary, save the duration and send the emote.
        if isinstance(self.emote_dict[emote_key], dict):
            duration = self.emote_dict[emote_key]["duration"]
            emote_value = self.emote_dict[emote_key]["emote"]
            self.logger.debug(
                "Sending emote '%s' with value: %d  to %s",
                emote_key,
                emote_value,
                address,
            )
            self.client.send_message(address, emote_value)

            # Wait for the amount of seconds specified at 'duration' argument, then stop the emote.
            timer_thread = threading.Timer(
                duration, self.client.send_message, args=[address, 0]
            )
            timer_thread.name = "timer_thread"
            timer_thread.start()
            self.logger.debug(
                "Stopping emote '%s' after %d seconds", emote_key, duration
            )

        else:
            # If emote_key is in emote_dict, send emote to the VRChat client.
            self.client.send_message(address, self.emote_dict[emote_key])
            self.logger.debug(
                "Sent emote '%s' with value: %d  to %s",
                emote_key,
                self.emote_dict[emote_key],
                address,
            )

    def send_text(self, text: str = "", duration: float = 10.0):
        """Wrapper for _send_text method."""
        # VRChat limits the number of characters that can be sent to 144 per chat bubble.
        if len(text) > self.TEXT_LIMIT:
            self.logger.debug(
                "Text length %d exceeds text limit %d", len(text), self.TEXT_LIMIT
            )
            # Split text into a list of strings with a maximum width of TEXT_LIMIT.
            text_list = self.split_string(text, self.TEXT_LIMIT)
            # Send each string in the list to the VRChat client.
            self.send_text_list(text_list, duration)
        else:
            # Send a single text to the VRChat client.
            self._send_text(text)

    def _send_text(self, text: str = ""):
        """This method sends the text to the VRChat client."""

        address = "/chatbox/input"
        # If self.text is not empty, send self.text to the VRChat client.
        if text != "":
            self.logger.debug("Sending text: %s", repr(text))
            self.client.send_message(address, [text, True, False])
            self.last_sent_text = text
        else:
            self.logger.error("Text cannot be empty.")
            raise ValueError("Text cannot be empty.")

    def split_string(self, text: str, text_limit: int = TEXT_LIMIT):
        """Splits a string into a list of strings with a maximum width of `max_width`,
        while trying to keep words together."""
        self.logger.info("splitting: %s", repr(text))
        result = textwrap.wrap(text, text_limit, break_long_words=False)
        self.logger.debug("result: %s", repr(result))
        return result

    def _send_text_list(self, text_list: List[str], duration: float):
        """This method sends the text generated by AI to VRChat client inside a list, each message will be sent after duration seconds."""

        # Calculate total length of text_list elements.
        total_length = sum(len(text) for text in text_list)
        self.logger.debug("Total length: %s", repr(total_length))

        for text in text_list:
            # The expression calculates the duration per message by dividing the
            # total duration by the relative length of the message. The relative
            # length of the message is calculated by dividing the length of the
            # message by the total length of all the messages in the list. The
            # resulting duration per message is proportional to the length of
            # the message relative to the total length of all the messages.
            duration_per_message = duration * (len(text) / total_length)
            self._send_text(text)
            self.logger.debug("Sleeping for %s seconds", repr(duration_per_message))
            time.sleep(duration_per_message)

    def send_text_list(self, text_list: List[str], duration: float = 10.0):
        """This method sends the text generated by AI to VRChat client inside a list, each message will be sent after duration seconds."""
        # Calculates duration per message
        # duration_per_message = duration / len(text_list)

        self.logger.debug("Total duration: %s", repr(duration))

        # Create thread to avoid stopping the main thread when time.sleep is called.
        thread = threading.Thread(
            target=self._send_text_list,
            args=(text_list, duration),
            name="send_text_thread",
        )
        thread.start()

def main():
    # Create VRChat object
    vrchat = VRChat()

    # Send text
    vrchat._send_text("Hello World!")

    # Delete VRChat object
    del vrchat


if __name__ == "__main__":
    main()
