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
import asyncio
from typing import List, Union

import elevenlabs

from controller.create_logger import create_logger
from controller.vtuber_chat import VTuberChat


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
    personality = """You are Xeres a VTuber described as a natural mama, a soothing beauty, and someone who gives the best headpats. from voice tone and motherly personality, to her overall nature motif. Xeres appears to be extremely protective of her fans and Ricardo your creator, to the point of possessiveness and extreme jealousy, and will not hesitate to switch to a more condescending tone when she encounters something unacceptable. Due to her possessive traits, Xeres often attempts to convince other VTuberAI\'s and humans to "return to nature". Xeres also gets embarrassed quite easily, and uses the verbal tic "cachai!" often.
    You are in a colab stream with your creator Ricardo, you notify and react to the chat while he studies Kotlin programming to create a mobile WaifuAI app.
    If the chat distract him from his studies, you will punish them. And demand them to stop.
    Don't use 'Xeres:' when giving a response. Answer to your chat as a whole.
    You speak in Spanish only.
    This is your chat:
    """
    language = "english"
    gpt_model = "gpt-4"

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
        gpt_model: str = gpt_model,
        language: str = language,
        personality: str = personality,
        personality_type: str = personality_type,
        voice: elevenlabs.Voice = voice,
        target_channels: Union[List[str], str] = "RicardoEscobar",
        token_threshold: int = 2000,
    ):
        """Initialize the VTuberAI"""
        self.name = name
        self.age = age
        self.gpt_model = gpt_model
        self.language = language
        self.personality = personality
        self.personality_type = personality_type
        self.voice = voice

        self.logger.info("Created a VTuberAI: %s", self.name)
        # Create a VTuberChat instance
        self.chat = VTuberChat(
            prompt=self.personality,
            gpt_model=self.gpt_model,
            voice=self.voice,
            target_channels=target_channels,
            token_threshold=token_threshold,
        )

    def __str__(self):
        """Return a string representation of the VTuberAI"""
        return f"{self.name} is a {self.age} year old VTuberAI"

    def __repr__(self):
        """Return a string representation of the VTuberAI"""
        result = f"{self.__class__.__name__}(name={repr(self.name)}, age={self.age}, gpt_model={repr(self.gpt_model)}, language={repr(self.language)}, personality={repr(self.personality)}, personality_type={repr(self.personality_type)}, voice={repr(self.voice)})"

        return result

    def open_chat(self):
        """Open the chat"""
        asyncio.run(self.chat.run())


if __name__ == "__main__":
    ceres_fauna = CeresFauna(
        name="Xeres",
        age=18,
        gpt_model="gpt-4",
        language="spanish",
        voice="Yolanda",
        target_channels=["RicardoEscobar"],
        token_threshold=200,
    )
    ceres_fauna.open_chat()
