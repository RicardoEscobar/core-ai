"""This module saves a natural voice to the core-ai database."""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    if str(root_folder) not in sys.path:
        sys.path.append(str(root_folder))

import pickle
import psycopg

from elevenlabs.api import Voice, VoiceSettings

from controller.create_logger import create_logger
from model.database import Database

# Create a logger
module_logger = create_logger(
    logger_name="model.save_natural_voice",
    logger_filename="save_natural_voice.log",
    log_directory="logs/database",
    add_date_to_filename=False,
)


def insert_natural_voice_data(
    name: str,
    short_name: str,
    voice_id: str,
    voice_object: Voice,
    connection: psycopg.Connection = None,
    protocol: int = pickle.HIGHEST_PROTOCOL,
):
    if connection is None:
        raise ValueError(
            "'connection' argument is 'None' Database connection is not established."
        )
    if isinstance(connection, psycopg.Connection) is False:
        raise TypeError("'connection' argument must be of type psycopg.Connection.")

    try:
        cursor = connection.cursor()
        insert_query_voice = """INSERT INTO public.voice_elevenlabs(
	name, short_name, voice_id, voice_object, pickle_protocol)
	VALUES (%s, %s, %s, %s, %s);"""

        binary_data = psycopg.Binary(
            pickle.dumps(voice_object, protocol=protocol)
        )
        cursor.execute(
            insert_query_voice,
            (
                name,
                short_name,
                voice_id,
                binary_data,
                protocol,
            ),
        )

        connection.commit()

    except psycopg.Error as error:
        module_logger.error("Error while inserting data: %s", error)
    finally:
        if connection:
            cursor.close()


def get_natural_voice_data(
    voice_id: str, connection: psycopg.Connection = None
) -> Voice:
    if connection is None:
        raise ValueError(
            "'connection' argument is 'None' Database connection is not established."
        )
    if isinstance(connection, psycopg.Connection) is False:
        raise TypeError("'connection' argument must be of type psycopg.Connection.")
    try:
        cursor = connection.cursor()
        select_query_voice = (
            """SELECT voice_object FROM public.voice_elevenlabs WHERE voice_id = %s;"""
        )
        cursor.execute(select_query_voice, (voice_id,))
        voice_object = cursor.fetchone()[0]
        return pickle.loads(voice_object)
    except psycopg.Error as error:
        module_logger.error("Error while inserting data: %s", error)
    finally:
        if connection:
            cursor.close()


def main():
    """Main function of the module."""
    # Create a database instance
    database = Database()
    connection = database.connection

    voice_object = Voice(
        voice_id="chQ8GR2cY20KeFjeSaXI",
        name="[ElevenVoices] Hailey - American Female Teen",
        category="generated",
        description="",
        labels={
            "accent": "american",
            "age": "young",
            "voicefrom": "ElevenVoices",
            "gender": "female",
        },
        samples=None,
        settings=VoiceSettings(stability=0.5, similarity_boost=0.75),
        design=None,
        preview_url="https://storage.googleapis.com/eleven-public-prod/PyUBusauIUbpupKTM31Yp4fHtgd2/voices/OgTivnXy9Bsc96AcZaQz/44dc6d49-cd44-4aad-a453-73a12c215702.mp3",
    )

    insert_natural_voice_data(
        name="[ElevenVoices] Hailey - American Female Teen",
        short_name="Lumina",
        voice_id="chQ8GR2cY20KeFjeSaXI",
        voice_object=voice_object,
        connection=connection,
    )
    module_logger.info("Natural voice data inserted successfully in core-ai database.")

    # Testing recovering the natural voice object
    voice_object = get_natural_voice_data(
        voice_id="chQ8GR2cY20KeFjeSaXI", connection=connection
    )

    print(f'\nVoice object =>\n{repr(voice_object)}')

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()
