import os
import psycopg
from dotenv import load_dotenv
from user.platform import Platform
from typing import List

load_dotenv()

# Connect to an existing database
connection = psycopg.connect(
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT')
)

# Create Platform objects
platform1 = Platform(
    name='Twitch', description="""1Twitch i"s' a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.""")
platform2 = Platform(
    name='YouTube', description='2YouTube is an American online video-sharing platform headquartered in San Bruno, California.')
platform3 = Platform(
    name='VRChat', description='3VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.')

# Save the platform objects into a list
platforms: List[Platform] = [platform1, platform2, platform3]
Platform.save_platforms(platforms, connection)

# Save the platform objects into the database
# for platform in platforms:
#     platform.save(connection)

# Create a cursor to perform database operations
cursor = connection.cursor()

query = """SELECT * from "user".platform;"""
cursor.execute(query)
all_rows = cursor.fetchall()
print(all_rows)

connection.close()
