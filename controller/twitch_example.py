# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os

from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio

from controller.waifuai.load_openai import load_openai

# Login into Twitch API
load_openai()

# Load Twitch API keys
# Set the Twitch API key
TWITCH_APP_ID = os.getenv("TWITCH_APP_ID")
TWITCH_APP_SECRET = os.getenv("TWITCH_APP_SECRET")

async def twitch_example():
    # initialize the twitch instance, this will by default also create a app authentication for you
    twitch = await Twitch(TWITCH_APP_ID, TWITCH_APP_SECRET)
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins='ricardoescobar'))
    # print the ID of your user or do whatever else you want with it
    print(f"""user id: {user.id}
user display name: {user.display_name}""")

# run this example
asyncio.run(twitch_example())