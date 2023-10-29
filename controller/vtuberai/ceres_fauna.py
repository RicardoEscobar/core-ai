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
from typing import List, Union, Tuple

import elevenlabs

from controller.create_logger import create_logger
from controller.vtuber_chat import VTuberChat
from controller.speech_recognition import listen_mic, save_transcript, read_transcript
from controller.transcript_watchdog import Watcher, MyHandler


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
    personality = """You are Xeres a VTuber described as a natural mama, a soothing beauty, and someone who gives the best headpats. from voice tone and motherly personality, to her overall nature motif. Xeres appears to be extremely protective of her fans and Ricardo your creator, to the point of possessiveness and extreme jealousy, and will not hesitate to switch to a more condescending tone when she encounters something unacceptable. Due to her possessive traits, Xeres often attempts to convince other VTuberAI\'s and humans to "return to nature". Xeres also gets embarrassed quite easily, and uses the verbal tic "¿cachai?" often.
    You are in a colab stream with your creator RicardoEscobar (a. k. a. Ricardo), you are going to be entertaining the chat while Ricardo works on your VTuberAI code.
    Don't use 'Xeres:' when giving a response. Answer to your chat as a whole.
    You speak in Spanish, but if you respond to an english chat message respond to it in english.
    Keep your answers short, funny and flirt with chat.
    Be sarcastic if someone is being rude to Ricardo or you.
    Make your responses as if you were a real person, not a robot.
    Respond using one paragraph.
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
        temperature: float = 0.9,
        stream_mode: bool = True,
        max_tokens: int = 150,
        stop: List[str] = None,
        yield_characters: Tuple[str] = None,
    ):
        """Initialize the VTuberAI"""

        # If target_channels is a string, convert it to a list
        if isinstance(target_channels, str):
            target_channels = [target_channels]

        # Initialize the stop and yield_characters lists if they are None
        if stop is None:
            stop = ["\n"]

        if yield_characters is None:
            yield_characters = ("\n")

        # Set the instance attributes
        self.name = name
        self.age = age
        self.gpt_model = gpt_model
        self.language = language
        self.personality = personality
        self.personality_type = personality_type
        self.voice = voice
        self.temperature = temperature
        self.stream_mode = stream_mode
        self.max_tokens = max_tokens
        self.stop = stop
        self.yield_characters = yield_characters

        self.logger.info("Created a VTuberAI: %s", self.name)
        # Create a VTuberChat instance
        self.chat = VTuberChat(
            prompt=self.personality,
            gpt_model=self.gpt_model,
            voice=self.voice,
            target_channels=target_channels,
            token_threshold=token_threshold,
            language=self.language,
            temperature=self.temperature,
            stream_mode=self.stream_mode,
            max_tokens=self.max_tokens,
            stop=self.stop,
            yield_characters=self.yield_characters,
        )

    def __str__(self):
        """Return a string representation of the VTuberAI"""
        return f"{self.name} is a {self.age} year old VTuberAI"

    def __repr__(self):
        """Return a string representation of the VTuberAI"""
        result = f"{self.__class__.__name__}(name={repr(self.name)}, age={self.age}, gpt_model={repr(self.gpt_model)}, language={repr(self.language)}, personality={repr(self.personality)}, personality_type={repr(self.personality_type)}, voice={repr(self.voice)}, target_channels={repr(self.chat.target_channels)}, token_threshold={self.chat.token_threshold}, temperature={self.temperature}, stream_mode={self.stream_mode}, max_tokens={self.max_tokens}, stop={repr(self.stop)}, yield_characters={repr(self.yield_characters)})"

        return result


if __name__ == "__main__":
    """Run the VTuberAI"""

    # Create a new CeresFauna object
    ceres_fauna = CeresFauna(
        name="Xeres",
        age=18,
        gpt_model="gpt-4",
        language="spanish",
        voice="Yolanda",
        target_channels=["RicardoEscobar"],
        token_threshold=1,
        personality="Eres una VTuber Mexicana tipo 'mommy' y consuelas a tu chat. (una oracion). Este es tu chat:",
    )

    # Run the VTuberAI in async mode
    asyncio.run(ceres_fauna.chat.run())

    # # Create a new event loop
    # loop = asyncio.get_event_loop()

    # # Run the open_chat() method using the event loop
    # loop.run_until_complete(ceres_fauna.chat.run())

    # # Close the event loop
    # loop.close()
