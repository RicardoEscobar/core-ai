"""Unit tests for the VRChat module."""
if __name__ == "__main__":
    import sys
    import os

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.append(ROOT_DIR)

import unittest
from unittest.mock import patch
import time

from controller.vrchat import VRChat
from controller.create_logger import create_logger

# Create logger
module_logger = create_logger(
    logger_name="tests.unit.test_vrchat",
    logger_filename="vrchat.log",
    log_directory="logs",
    add_date_to_filename=False,
)


class TestVRChat(unittest.TestCase):
    """Test the vrchat module."""

    def setUp(self) -> None:
        """Set up the test."""

        # Create VRChat object
        self.vrchat = VRChat()

        # Create logger
        self.logger = module_logger
        self.logger.debug("Logging configuration for test_vrchat finished.")

    def tearDown(self) -> None:
        """Tear down the test."""

        # Delete VRChat object
        del self.vrchat

        # Delete logger
        self.logger.debug("Logger configuration for test_vrchat deleted.")
        del self.logger

    @patch("pythonosc.udp_client.SimpleUDPClient.send_message")
    def test_send_text(self, mock_send_message):
        """Test the send_text method."""

        # Assert that last_sent_text is changed after sending text.
        self.vrchat._send_text("Hello World! from test_vrchat")
        expected_last_sent_text = "Hello World! from test_vrchat"
        self.assertEqual(self.vrchat.last_sent_text,expected_last_sent_text)

        # Assert that send_message is called.
        mock_send_message.assert_called_with("/chatbox/input", [expected_last_sent_text, True, False])

        # Assert that ValueError is raised when sending empty text.
        with self.assertRaises(ValueError):
            self.vrchat._send_text()

    def test_split_string(self):
        """Test the split_string method."""

        text = """Loona is a hellhound with a wolf-like appearance. She has a pointed, dog-like muzzle with sharp and pointy teeth, and a dark grey nose. Her eyes have red sclera with white irises, and she wears black winged eyeliner. She also has a piercing on her right eyebrow with a black hoop for jewelry.

Her fur is white with grey encircling her face, grey patches on her shoulders, and long, voluminous silver hair swept to the side to reveal her dark grey ears - the left of which is pierced with two small, black hoop earrings, while the right is ragged. She has a large, dark grey bushy tail with white on the underside.

Her outfit features a spiked black choker. Her tattered grey, off-the-shoulder crop-top is held up at the neckline by a series of crisscross spaghetti-straps that form an inverted pentagram. She wears black shorts that are tattered at the hems, with a white crescent moon detail on the right side. Loona accessorizes with fingerless gloves and black toeless thigh-high stockings, with her black claws protruding due to her digitigrade stance.

As a teenager, she appears very largely similar to her current appearance, except the spot where her right ear is ragged as an adult used to have two black hoop earrings in it just like her left ear, implying it was possibly ripped out that way. The only other difference is her outfit; instead of her gray pentagram crop-top, she wears a red off-the-shoulder long sleeve top with a black skull design, and instead of her toeless thigh-high stockings, she wears distressed black stockings that go up to her waist.

She is the tallest and the only non-imp member of I.M.P.

Human Disguise
Loona's human disguise is greatly similar to her hellhound form, albeit now she takes on the appearance of a goth teenager. Her eye colors are inverted, as she has white sclera with red irises and has a visible belly button which she lacks in hellhound form. She shrinks down from her demon form, appearing to be of average height compared to most humans in this form and somewhat slimmer than normal.

She retains the same outfit as before, but with the addition of black knee-high socks and high-top sneakers and black lipstick. Her choker also loses the spikes, and in place of her torn right ear, she now has two earrings on each ear. Her head is shaved on the right side."""

        expected_split_strings = [
            "Loona is a hellhound with a wolf-like appearance. She has a pointed, dog-like muzzle with sharp and pointy teeth, and a dark grey nose. Her eyes",
            "have red sclera with white irises, and she wears black winged eyeliner. She also has a piercing on her right eyebrow with a black hoop for",
            "jewelry.  Her fur is white with grey encircling her face, grey patches on her shoulders, and long, voluminous silver hair swept to the side to",
            "reveal her dark grey ears - the left of which is pierced with two small, black hoop earrings, while the right is ragged. She has a large, dark",
            "grey bushy tail with white on the underside.  Her outfit features a spiked black choker. Her tattered grey, off-the-shoulder crop-top is held up",
            "at the neckline by a series of crisscross spaghetti-straps that form an inverted pentagram. She wears black shorts that are tattered at the",
            "hems, with a white crescent moon detail on the right side. Loona accessorizes with fingerless gloves and black toeless thigh-high stockings,",
            "with her black claws protruding due to her digitigrade stance.  As a teenager, she appears very largely similar to her current appearance,",
            "except the spot where her right ear is ragged as an adult used to have two black hoop earrings in it just like her left ear, implying it was",
            "possibly ripped out that way. The only other difference is her outfit; instead of her gray pentagram crop-top, she wears a red off-the-shoulder",
            "long sleeve top with a black skull design, and instead of her toeless thigh-high stockings, she wears distressed black stockings that go up to",
            "her waist.  She is the tallest and the only non-imp member of I.M.P.  Human Disguise Loona's human disguise is greatly similar to her hellhound",
            "form, albeit now she takes on the appearance of a goth teenager. Her eye colors are inverted, as she has white sclera with red irises and has a",
            "visible belly button which she lacks in hellhound form. She shrinks down from her demon form, appearing to be of average height compared to most",
            "humans in this form and somewhat slimmer than normal.  She retains the same outfit as before, but with the addition of black knee-high socks and",
            "high-top sneakers and black lipstick. Her choker also loses the spikes, and in place of her torn right ear, she now has two earrings on each",
            "ear. Her head is shaved on the right side.",
        ]

        # Split a string into a list of strings
        actual_split_strings = self.vrchat.split_string(text)

        # Assert that split_string returns a list of strings.
        self.assertIsInstance(actual_split_strings, list)

        # Assert that each element in the list is a string
        self.assertTrue(all(isinstance(s, str) for s in actual_split_strings))

        # Assert the contents of the list against the expected list.
        self.assertListEqual(actual_split_strings, expected_split_strings)

    @patch("pythonosc.udp_client.SimpleUDPClient.send_message")
    def test_send_text_list(self, mock_send_message):
        """Test the _send_text_list method."""

        # Create test list
        test_list = [
            "1Hello World!",
            "2Hello World!",
            "3Hello World!",
            "4Hello World!",
            "5Hello World!",
        ]

        expected_split_strings = [
            "Loona is a hellhound with a wolf-like appearance. She has a pointed, dog-like muzzle with sharp and pointy teeth, and a dark grey nose. Her eyes",
            # "have red sclera with white irises, and she wears black winged eyeliner. She also has a piercing on her right eyebrow with a black hoop for",
            # "jewelry.  Her fur is white with grey encircling her face, grey patches on her shoulders, and long, voluminous silver hair swept to the side to",
            # "reveal her dark grey ears - the left of which is pierced with two small, black hoop earrings, while the right is ragged. She has a large, dark",
            # "grey bushy tail with white on the underside.  Her outfit features a spiked black choker. Her tattered grey, off-the-shoulder crop-top is held up",
            # "at the neckline by a series of crisscross spaghetti-straps that form an inverted pentagram. She wears black shorts that are tattered at the",
            # "hems, with a white crescent moon detail on the right side. Loona accessorizes with fingerless gloves and black toeless thigh-high stockings,",
            # "with her black claws protruding due to her digitigrade stance.  As a teenager, she appears very largely similar to her current appearance,",
            # "except the spot where her right ear is ragged as an adult used to have two black hoop earrings in it just like her left ear, implying it was",
            # "possibly ripped out that way. The only other difference is her outfit; instead of her gray pentagram crop-top, she wears a red off-the-shoulder",
            # "long sleeve top with a black skull design, and instead of her toeless thigh-high stockings, she wears distressed black stockings that go up to",
            # "her waist.  She is the tallest and the only non-imp member of I.M.P.  Human Disguise Loona's human disguise is greatly similar to her hellhound",
            # "form, albeit now she takes on the appearance of a goth teenager. Her eye colors are inverted, as she has white sclera with red irises and has a",
            # "visible belly button which she lacks in hellhound form. She shrinks down from her demon form, appearing to be of average height compared to most",
            # "humans in this form and somewhat slimmer than normal.  She retains the same outfit as before, but with the addition of black knee-high socks and",
            # "high-top sneakers and black lipstick. Her choker also loses the spikes, and in place of her torn right ear, she now has two earrings on each",
            "ear. Her head is shaved on the right side.",
        ]

        # Create test duration
        duration_seconds = 10

        # Send test list
        self.vrchat.send_text_list(expected_split_strings, duration_seconds)
        self.logger.debug("End of test_send_text_list")

        # Assert that send_message is called for each element in the list. Commented out because it takes too long.
        # time.sleep(duration_seconds + 1)
        # self.assertEqual(mock_send_message.call_count, len(expected_split_strings))

    @patch("pythonosc.udp_client.SimpleUDPClient.send_message")
    def test_send_vrc_emote(self, mock_send_message):
        """Test the send_vrc_emote method."""

        # Assert that send_message is called.
        self.vrchat.send_vrc_emote("wave")
        mock_send_message.assert_called_with("/avatar/parameters/VRCEmote", 1)

        # Assert that if an emote with a dictionary as value is used, save the duration and send the emote.
        # The applause emote has a duration of 5 seconds.
        self.vrchat.send_vrc_emote("applause")
        mock_send_message.assert_called_with("/avatar/parameters/VRCEmote", 2)




if __name__ == "__main__":
    unittest.main()
