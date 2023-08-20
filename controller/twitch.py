if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os
from typing import Union

from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

from controller.waifuai.load_openai import load_openai


# ANSI escape codes for text color
class TextColor:
    # BLACK = '\033[30m'
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"  # Reset to default color

    CHANNEL_COLOR_DICT = {
        "YashiroMiuna": RED,
        "nootie": GREEN,
        "gohuntleo": YELLOW,
        "ironmouse": BLUE,
        "nyanners": MAGENTA,
        "default": CYAN,
        "reset": RESET,
    }


# Login into Twitch API
load_openai()

# Set the Twitch API key
TWITCH_APP_ID = os.getenv("TWITCH_APP_ID")
TWITCH_APP_SECRET = os.getenv("TWITCH_APP_SECRET")

APP_ID = TWITCH_APP_ID
APP_SECRET = TWITCH_APP_SECRET
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = [
    "YashiroMiuna",
    "nootie",
    "gohuntleo",
    "ironmouse",
    "nyanners",
    "Revuwu",
]


def save_log(msg: Union[ChatMessage, ChatSub, ChatCommand]):
    """Save the message to a file for each channel, create the chat folder if it doesn't exist"""
    if isinstance(msg, ChatMessage):
        message = f"__{msg.user.name}__: {msg.text}"
    elif isinstance(msg, ChatSub):
        message = f"__New subscription: {msg.room.name}__, Type: {msg.sub_plan}, Message: {msg.sub_message}"
    elif isinstance(msg, ChatCommand):
        message = f"__{msg.user.name}:Command__: {msg.text}"
    else:
        raise TypeError(
            f"msg must be of type ChatMessage, ChatSub, or ChatCommand, not {type(msg)}")

    if not os.path.exists("chat"):
        os.makedirs("chat")
    with open(f"chat/{msg.room.name}.md", "a", encoding="utf-8") as chat_log_file:
        chat_log_file.write(f"{message}\n\n")


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print("Bot is ready for work, joining channels")
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    # assign color to text based on channel
    if msg.room.name in TextColor.CHANNEL_COLOR_DICT:
        color = TextColor.CHANNEL_COLOR_DICT[msg.room.name]
    else:
        color = TextColor.CHANNEL_COLOR_DICT["default"]

    # print the message to the console
    print(
        f"{color}{msg.room.name}:{msg.user.display_name}:{TextColor.RESET} {msg.text}"
    )

    # Save the message to a file for each channel, create the chat folder if it doesn't exist
    save_log(msg)


# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    message = f"New subscription: {sub.room.name}, Type: {sub.sub_plan}, Message: {sub.sub_message}"
    print(message)
    save_log(sub)


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply("you did not tell me what to reply with")
    else:
        await cmd.reply(f"{cmd.user.name}: {cmd.parameter}")
        save_log(cmd)


# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command("reply", test_command)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input("press ENTER to stop\\n")
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


# lets run our setup
asyncio.run(run())
