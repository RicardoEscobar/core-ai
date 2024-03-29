"""This module will handle the Twitch chat and give access to the VTuberAI to chat with the viewers"""
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os
from typing import Union, List, Tuple
import logging
import asyncio

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import tiktoken
import elevenlabs

from controller.load_openai import load_openai
from controller.create_logger import create_logger
from controller.stream_completion import StreamCompletion


# Create a logger instance
module_logger = create_logger(
    logger_name="controller.vtuber_chat",
    logger_filename="vtuber_chat.log",
    log_directory="logs",
    console_logging=True,
    console_log_level=logging.INFO,
)


# Login into Twitch API
load_openai()


class VTuberChat:
    """This class will handle the Twitch chat"""

    # Set the Twitch API key
    twitch_app_id = os.getenv("TWITCH_APP_ID")
    twitch_app_secret = os.getenv("TWITCH_APP_SECRET")

    # Assign module logger
    logger = module_logger

    # Create default voice
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

    def __init__(
        self,
        prompt: str,
        gpt_model: str,
        target_channels: Union[str, List[str]] = "RicardoEscobar",
        voice: Union[elevenlabs.Voice, str] = "Larissa",
        token_threshold: int = 2000,
        language: str = "es-ES",
        temperature: float = 0.9,
        stream_mode: bool = True,
        max_tokens: int = 150,
        stop: List[str] = None,
        yield_characters: Tuple[str] = None,
    ):
        """Initialize the Twitch chat"""

        self.logger.info("Initializing VTuberChat class.")
        if stop is None:
            stop = ["\n"]

        if yield_characters is None:
            yield_characters = (".", "?", "!", "\n", ":", ";")

        # Set attributes
        self.user_scope = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.target_channels = target_channels
        self._chat_log = dict()
        self.gpt_model = gpt_model
        self._token_count = 0
        self._token_threshold = token_threshold
        self.voice = voice
        self.prompt = prompt
        self.initial_prompt = prompt
        self.language = language
        self.temperature = temperature
        self.stream_mode = stream_mode
        self.max_tokens = max_tokens
        self.stop = stop
        self.yield_characters = yield_characters
        self._transcription = list()
        self.microphone_username = "RicardoEscobar"

        self.stream_completion = StreamCompletion(
            self.voice,
            self.prompt,
            self.gpt_model,
            temperature=temperature,
            stream_mode=self.stream_mode,
            max_tokens=self.max_tokens,
            stop=self.stop,
            yield_characters=self.yield_characters,
        )

    @property
    def transcription(self):
        """Return the transcription list"""
        return self._transcription

    @transcription.setter
    def transcription(self, value):
        """Set the transcription list"""
        self._transcription = value

        # Append all elements of the transcription list to the prompt, as a message from the self.microphone_username
        chat_message = (
            "\n" + self.microphone_username + ": " + " ".join(self._transcription)
        )

        # Don't allow duplicates: if chat_message does not already exist in self.prompt already, add it to the prompt.
        # if chat_message not in self.prompt:
        # print(f"chat_message={chat_message}")
        self.prompt += chat_message

        # Count the number of tokens, and add it to the token count
        self.token_count += self.get_token_count(chat_message, self.gpt_model)

    @property
    def token_count(self):
        """Return the token count"""
        return self._token_count

    @token_count.setter
    def token_count(self, value: int):
        """Set the token count"""
        self._token_count = value
    
    async def run_trigger_vtuber_interaction(self):
        """Run the trigger_vtuber_interaction method"""
        tokens_left = self.token_threshold - self._token_count

        # Create a message to display the number of tokens left
        message = f"Siguiente respuesta en: {tokens_left} tokens."
        self.logger.info(message)

        # Save the number of tokens left into a tokens_left.txt file
        with open("tokens_left.txt", "w", encoding="utf-8") as tokens_left_file:
            tokens_left_file.write(message)

        # When the token count exceeds the threshold, trigger a VTuber interaction with the chat
        if self._token_count >= self._token_threshold:
            self.logger.info("Token count exceeded the threshold, saving the chat log.")

        # Trigger a VTuber interaction with the chat, using a coroutine task
        try:
            # Wait for the task to complete
            task = asyncio.create_task(self.trigger_vtuber_interaction(
                    prompt=self.prompt,
                    gpt_model=self.gpt_model,
                    voice=self.voice,
                    audio_output_dir="./audio",
                ))
            await task
        except TypeError as error:
            self.logger.error(error)

        # Reset prompt
        self.prompt = self.initial_prompt

        # Reset the token count
        self._token_count = 0

        # Reset the transcription list
        self.transcription = list()

    @token_count.deleter
    def token_count(self):
        """Delete the token count"""
        self._token_count = 0

    @property
    def token_threshold(self):
        """Return the token threshold"""
        return self._token_threshold

    @token_threshold.setter
    def token_threshold(self, value):
        """Set the token threshold"""
        self._token_threshold = value

    @token_threshold.deleter
    def token_threshold(self):
        """Delete the token threshold"""
        self._token_threshold = 2000

    @property
    def chat_log(self):
        """Return the chat log dictionary"""
        return self._chat_log

    @chat_log.setter
    def chat_log(self, value):
        """Set the chat log dictionary"""
        self._chat_log = value

    @chat_log.deleter
    def chat_log(self):
        """Delete the chat log dictionary"""
        self._chat_log = dict()

    def save_log(self, msg: Union[ChatMessage, ChatSub, ChatCommand]):
        """Save the message to a file for each channel, create the chat folder if it doesn't exist"""
        if isinstance(msg, ChatMessage):
            message = f"__{msg.user.name}__: {msg.text}"
        elif isinstance(msg, ChatSub):
            message = f"__New subscription: {msg.room.name}__, Type: {msg.sub_plan}, Message: {msg.sub_message}"
        elif isinstance(msg, ChatCommand):
            message = f"__{msg.user.name}:Command__: {msg.text}"
        else:
            raise TypeError(
                f"msg must be of type ChatMessage, ChatSub, or ChatCommand, not {type(msg)}"
            )

        if not os.path.exists("chat"):
            os.makedirs("chat")
        with open(f"chat/{msg.room.name}.md", "a", encoding="utf-8") as chat_log_file:
            chat_log_file.write(f"{message}\n\n")

    async def save_chat_log(self, msg: Union[ChatMessage, ChatSub, ChatCommand]) -> None:
        """Save the message to a dictionary for each channel"""

        # Check if the message is a ChatMessage, ChatSub, or ChatCommand
        if isinstance(msg, (ChatMessage, ChatSub, ChatCommand)):
            self.logger.debug("Saving message to chat log dictionary: %s", msg)
        else:
            raise TypeError(
                "msg must be of type ChatMessage, ChatSub, or ChatCommand, not {}".format(
                    type(msg)
                )
            )

        try:
            # Save the message to the chat log dictionary
            self.chat_log[msg.room.name].append(msg)
        except KeyError:
            # Create a new chat log list for the channel
            self.chat_log[msg.room.name] = [msg]
            self.logger.error("KeyError: %s, a new key was created.", msg.room.name)
        finally:
            text = "\n{}: {}".format(msg.user.name, msg.text)

            # Add text to the prompt
            self.prompt += text

            # Assign a new value to the token_count property and await for the setter to finish
            self.token_count += self.get_token_count(text, self.gpt_model)

            # Trigger a VTuber interaction with the chat if the token count exceeds the threshold
            await self.run_trigger_vtuber_interaction()


    # this will be called when the event READY is triggered, which will be on bot start
    async def on_ready(self, ready_event: EventData):
        self.logger.info("Bot is ready for work, joining channels")
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(self.target_channels)
        # you can do other bot initialization things in here

    # this will be called whenever a message in a channel was send by either the bot OR another user
    async def on_message(self, msg: ChatMessage):
        # assign yellow color username and channel name.
        yellow = "\033[33m"

        # Assign reset color to reset the color to default.
        reset_color = "\033[0m"

        # print the message to the console
        self.logger.info(
            "%s%s:%s:%s %s",
            yellow,
            msg.room.name,
            msg.user.display_name,
            reset_color,
            msg.text,
        )

        # Save the message to a file for each channel, create the chat folder if it doesn't exist
        self.save_log(msg)

        # Save the message to a dictionary for each channel
        await self.save_chat_log(msg)

    # this will be called whenever someone subscribes to a channel
    async def on_sub(self, sub: ChatSub):
        """This will be called whenever someone subscribes to a channel"""

        # assign yellow color username and channel name.
        yellow = "\033[33m"

        # Assign reset color to reset the color to default.
        reset_color = "\033[0m"

        message = f"{yellow}New subscription: {sub.room.name}, Type: {sub.sub_plan}, Message:{reset_color} {sub.sub_message}"

        # print the message to the console
        self.logger.info(message)

        # Save the message to a file for each channel, create the chat folder if it doesn't exist
        self.save_log(sub)

        # Save the message to a dictionary for each channel
        await self.save_chat_log(sub)

    # this will be called whenever the !reply command is issued
    async def test_command(self, cmd: ChatCommand):
        """This will be called whenever the !reply command is issued"""

        # assign yellow color username and channel name.
        yellow = "\033[33m"

        # Assign reset color to reset the color to default.
        reset_color = "\033[0m"

        message = f"{yellow}{cmd.user.name}:{reset_color} {cmd.parameter}"

        # print the message to the console
        self.logger.info(message)

        if len(cmd.parameter) == 0:
            await cmd.reply("you did not tell me what to reply with")
        else:
            await cmd.reply(message)

            # Save the message to a file for each channel, create the chat folder if it doesn't exist
            self.save_log(cmd)

            # Save the message to a dictionary for each channel
            await self.save_chat_log(cmd)

    async def run(self):
        """Run the bot to listen mic and read chat at the same time... in concurrent mode really"""

        # Create two tasks that run the main() function concurrently
        read_chat_task = asyncio.create_task(self.read_chat())

        # Wait for the read_chat_task to complete
        await read_chat_task

    # this is where we set up the bot
    async def read_chat(self):
        """Read the chat"""
        # set up twitch api instance and add user authentication with some scopes
        twitch = await Twitch(self.twitch_app_id, self.twitch_app_secret)
        auth = UserAuthenticator(twitch, self.user_scope)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, self.user_scope, refresh_token)

        # create chat instance
        chat = await Chat(twitch)

        # register the handlers for the events you want
        # listen to when the bot is done starting up and ready to join channels
        chat.register_event(ChatEvent.READY, self.on_ready)
        # listen to chat messages
        chat.register_event(ChatEvent.MESSAGE, self.on_message)
        # listen to channel subscriptions
        chat.register_event(ChatEvent.SUB, self.on_sub)
        # there are more events, you can view them all in this documentation

        # you can directly register commands and their handlers, this will register the !reply command
        chat.register_command("reply", self.test_command)

        # we are done with our setup, lets start this bot up!
        chat.start()

        # lets run till we press enter in the console
        try:
            input("Press enter to stop the bot...\n")
        except KeyboardInterrupt:
            print("Stopped listening.")
        finally:
            # now we can close the chat bot and the twitch api client
            chat.stop()
            await twitch.close()

    def get_token_count(self, text: str, gpt_model: str = None) -> int:
        """Return the number of tokens given a text and a GPT model"""
        if gpt_model is None:
            gpt_model = self.gpt_model

        # To get the tokeniser corresponding to a specific model in the OpenAI API:
        encoding = tiktoken.encoding_for_model(gpt_model)

        # Encode a string into tokens
        tokens = encoding.encode(text)

        # Count the number of tokens
        num_tokens = len(tokens)

        return num_tokens

    async def trigger_vtuber_interaction(
        self,
        prompt: str = None,
        gpt_model: str = None,
        voice: Union[elevenlabs.Voice, str] = None,
        audio_output_dir: str = ".",
    ):
        """Trigger a VTuber interaction with the chat
        args:
            prompt: The prompt to use for the VTuber interaction.
            gpt_model: The GPT model to use for the VTuber interaction.
            voice: The voice to use for the VTuber interaction.
            audio_dir_path: The directory where the audio files will be saved.
        throws:
            TypeError: If voice is not of type elevenlabs.Voice or str.
        """

        # Set default values
        if prompt is None:
            prompt = self.prompt

        if gpt_model is None:
            gpt_model = self.gpt_model

        if voice is None:
            voice = self.voice

        self.logger.info("Triggering a VTuber interaction with the chat.")

        if isinstance(voice, elevenlabs.Voice):
            self.stream_completion.generate_completion(
                persona=prompt,
                gpt_model=gpt_model,
                voice=voice,
                audio_output_dir=audio_output_dir,
            )
        elif isinstance(voice, str):
            self.logger.info("Generating Microsoft AI Speech completion.")
            self.logger.info("prompt: %s", prompt)
            while True:
                try:
                    await self.stream_completion.generate_microsoft_ai_speech_completion(
                        prompt=prompt,
                        gpt_model=gpt_model,
                        selected_voice=voice,
                        audio_output_dir=audio_output_dir,
                    )
                except Exception as exception:
                    module_logger.error(exception)
                    continue
                else:
                    break
        else:
            self.logger.error(
                "voice must be of type elevenlabs.Voice or str, not %s", type(voice)
            )
            raise TypeError(
                f"voice must be of type elevenlabs.Voice or str, not {type(voice)}"
            )


################### Test code ###################
def main():
    # lets run our setup
    vtuber_chat = VTuberChat(prompt="Hola", gpt_model="gpt-4")
    asyncio.run(vtuber_chat.read_chat())


if __name__ == "__main__":
    main()
