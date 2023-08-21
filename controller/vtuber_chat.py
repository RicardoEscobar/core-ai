"""This module will handle the Twitch chat and give access to the VTuberAI to chat with the viewers"""
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os
from typing import Union, List
import logging

from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

from controller.load_openai import load_openai
from controller.create_logger import create_logger


# Create a logger instance
module_logger = create_logger(
    logger_name="controller.vtuber_chat",
    logger_filename="vtuber_chat.log",
    log_directory="logs",
    console_logging=False,
    console_log_level=logging.INFO,
)


# Login into Twitch API
load_openai()


########################################################################################################################
# Define a Twitch class to migrate the functions into a class for better organization
class VTuberChat:
    """This class will handle the Twitch chat"""

    # Set the Twitch API key
    twitch_app_id = os.getenv("TWITCH_APP_ID")
    twitch_app_secret = os.getenv("TWITCH_APP_SECRET")

    # Assign module logger
    logger = module_logger

    def __init__(self, target_channels: Union[str, List[str]] = "RicardoEscobar"):
        """Initialize the Twitch chat"""

        self.logger.info("Initializing VTuberChat class.")
        self.user_scope = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.target_channels = target_channels

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

    # this will be called whenever someone subscribes to a channel
    async def on_sub(self, sub: ChatSub):
        message = f"New subscription: {sub.room.name}, Type: {sub.sub_plan}, Message: {sub.sub_message}"
        print(message)
        self.save_log(sub)

    # this will be called whenever the !reply command is issued
    async def test_command(self, cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("you did not tell me what to reply with")
        else:
            await cmd.reply(f"{cmd.user.name}: {cmd.parameter}")
            self.save_log(cmd)

    # this is where we set up the bot
    async def run(self):
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
            input("press ENTER to stop\\n")
        finally:
            # now we can close the chat bot and the twitch api client
            chat.stop()
            await twitch.close()


################### Test code ###################
def main():
    # lets run our setup
    vtuber_chat = VTuberChat()
    asyncio.run(vtuber_chat.run())


if __name__ == "__main__":
    main()
