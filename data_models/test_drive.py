import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Connect to an existing database
conn = psycopg2.connect(
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT')
)

# Create a cursor to perform database operations
cur = conn.cursor()

query = """SELECT "user".insert_platform('Twitch', 'Twitch (Twitch.tv) is an online live streaming video platform with a focus on gaming. The name Twitch comes from the term twitch gaming, which refers to fast action games that test reflexes, such as first person shooter games. Twitch is part of Twitch Interactive and is a subsidiary of Amazon.');"""

# Run SELECT query, saving the results in a variable.
cur.execute(query)
conn.commit()

first_row = cur.fetchone()
print(first_row)

query = """SELECT * from "user".platform;"""
cur.execute(query)
first_row = cur.fetchone()
print(first_row)

conn.close()
