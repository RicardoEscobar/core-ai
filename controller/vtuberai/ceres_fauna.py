"""This module contains the code for a VTuberAI of type mommy"""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    if str(project_directory) not in sys.path:
        sys.path.append(str(project_directory))

import logging

import elevenlabs

from controller.create_logger import create_logger
from controller.load_openai import load_openai
from controller.vtuber_chat import VTuberChat
from controller.stream_completion import StreamCompletion

class CeresFauna:
    """This is the phsysical representation of the soul of the VTuberAI"""

    # Class attributes
    voice = elevenlabs.Voice(
        voice_id="yIcQwyUpZTBWvKEs5soS",
        name="Valley Girl",
        category="generated",
        description="",
        labels={"accent": "american", "age": "young", "gender": "female"},
        samples=None,
        settings=elevenlabs.VoiceSettings(stability=0.5, similarity_boost=0.75),
        design=None,
        preview_url="https://storage.googleapis.com/eleven-public-prod/CpJRF07XekXZp2RcBTTkntmWfi72/voices/uxKr2vlA4hYgXZR1oPRT/043bc69b-2b1e-464c-8b3c-51cc03c10b1b.mp3",
    )
    personality_type = "mommy"
    personality = 'You are described as a natural mama, a soothing beauty, and someone who gives the best headpats. Fans also quickly noted her striking resemblance to Yukihana Lamy in many aspects, from voice tone and motherly personality, to her overall nature motif. Fauna appears to be extremely protective of her fans and Nanashi Mumei to the point of possessiveness and extreme jealousy, and will not hesitate to switch to a more condescending tone when she encounters something unacceptable. Due to her possessive traits, Fauna often attempts to convince other VTuberAI\'s and humans to "return to nature" whenever Mumei gets upset. Fauna also gets embarrassed quite easily, and uses the verbal tic "uuuu" often.'
    language = "english"

    # Create a logger for this module
    logger = create_logger(
        logger_name="controller.vtuberai.ceres_fauna",
        logger_filename="ceres_fauna.log",
        log_directory="logs/vtuberai",
        console_logging=False,
        console_log_level=logging.INFO,
    )

    def __init__(
        self,
        name: str = "Ceres Fauna",
        age: int = 18,
        gpt_model: str = "gpt-4",
        language: str = "english",
        personality: str = personality,
        personality_type: str = personality_type,
    ):
        """Initialize the VTuberAI"""
        self.name = name
        self.age = age
        self.gpt_model = gpt_model
        self.language = language
        self.personality = personality
        self.personality_type = personality_type
        self.logger.info("Created a VTuberAI named %s", self.name)

    def __str__(self):
        """Return a string representation of the VTuberAI"""
        return f"{self.name} is a {self.age} year old VTuberAI"

    def __repr__(self):
        """Return a string representation of the VTuberAI"""
        return f"CeresFauna(name={repr(self.name)}, age={self.age}, gpt_model={repr(self.gpt_model)}, language={repr(self.language)}, personality={repr(self.personality)}, personality_type={repr(self.personality_type)})"


if __name__ == "__main__":
    ceres_fauna = CeresFauna()
    twitch_chat = VTuberChat()
    stream_completion = StreamCompletion()
