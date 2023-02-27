"""
Unit tests for the platform module.
"""
import logging
import os
import unittest
import psycopg
from dotenv import load_dotenv
import model.user.platform
from model.user.platform import Platform

# create logger with 'test_platform'
logger = logging.getLogger('test_platform')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
file_handler = logging.FileHandler('logs/test_platform.log')
file_handler.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s')

file_handler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(file_handler)


class TestPlatform(unittest.TestCase):
    """
    This class is used to test the platform module.
    """

    @classmethod
    def setUpClass(cls):
        """
        This method is used to set up the test environment.
        """
        load_dotenv()

        # Connect to an existing database
        cls.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        cls.DROP_TABLE = """DROP TABLE IF EXISTS "user".platform CASCADE;"""
        cls.CREATE_TABLE = """CREATE TABLE IF NOT EXISTS "user".platform
(
    id bigserial NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id),
    UNIQUE (name)
);"""

        cls.RESET_SEQUENCE = """-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('"user".platform', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "user".platform;
"""
        cls.TRUNCATE_TABLE = """TRUNCATE TABLE "user".platform CASCADE;"""

    @classmethod
    def tearDownClass(cls):
        """
        This method is used to tear down the test environment.
        """
        # Open a cursor to perform database operations
        with cls.connection.cursor() as cursor:
            cursor.execute(cls.DROP_TABLE)
            cursor.execute(cls.CREATE_TABLE)
            cursor.execute(cls.RESET_SEQUENCE)
            # cursor.execute(TRUNCATE_TABLE)
            cls.connection.commit()

        # Close the connection
        cls.connection.close()

    def setUp(self):
        """
        This method is used to set up the test environment.
        """
        self.connection = self.__class__.connection

        # Create Platform objects
        self.platform1 = Platform(
            name='Twitch', description="""Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.""")
        self.platform2 = Platform(
            name='YouTube', description='YouTube is an American online video-sharing platform headquartered in San Bruno, California.')
        self.platform3 = Platform(
            name='VRChat', description='VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.')

        # Save the platform objects into a list
        self.platforms = [self.platform1,  self.platform2,  self.platform3]

        # Open a cursor to perform database operations
        self.connection = self.__class__.connection
        with self.connection.cursor() as cursor:
            cursor.execute(self.DROP_TABLE)
            cursor.execute(self.CREATE_TABLE)
            cursor.execute(self.RESET_SEQUENCE)
            # cursor.execute(TRUNCATE_TABLE)
            self.connection.commit()

    def test_platform_str_repr(self):
        """
        This method is used to test the platform data model.
        """
        # Test the __str__ method
        expected = """(DEFAULT, $$Twitch$$, $$Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.$$)"""
        self.assertEqual(str(self.platform1), expected)

        # Test the __repr__ method
        expected = """Platform(_id=None, name='Twitch', description='Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.')"""
        self.assertEqual(repr(self.platform1), expected)

        logger.info('test_platform_str_repr: PASS')

    def test_platform_save(self):
        """
        This method is used to test the platform save method.
        """
        # Test the save method
        for i, platform in enumerate(self.platforms, start=1):
            platform.save(self.connection)
            # Assert that the platform objects are saved into the database.
            self.assertEqual(platform._id, i)

        # Assert that the platform objects are updated into the database when there is a conflict on the name column.
        expected = """Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon, and it's great!."""
        platform_updated = Platform('Twitch', expected)
        platform_updated.save(self.connection)
        self.assertEqual(platform_updated.description, expected)

        logger.info('test_platform_save: PASS')

    def test_platform_load(self):
        """
        This method is used to test the platform load method.
        """
        # Test the get_id method
        for expected_id, platform in enumerate(self.platforms, start=1):
            platform.save(self.connection)
            # Get id's from the database
            platform_id = platform.load(self.connection)
            # Assert that the platform objects got their id's from the database.
            self.assertEqual(platform_id, expected_id)

        # Assert that the platform objects trhow an exception when the name is not found in the database.
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')

        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):
            platform.load(self.connection)

        logger.info('test_platform_load: PASS')

    def test_platform_delete(self):
        """
        This method is used to test the platform delete method.
        """
        # Test the delete method
        for platform in self.platforms:
            platform.save(self.connection)
            platform.delete(self.connection)
            # Assert that the platform objects are deleted from the database.
            logger.debug(
                """Platform %s: '%s' deleted from the database.""", platform.id, platform.name)
            self.assertIsNone(platform._id)
        logger.info('Platforms deleted from the database.')

        # Assert that the platform objects throw an exception when the name is not found in the database.
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')
        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):
            platform.delete(self.connection)

        logger.info('test_platform_delete: PASS')

    def test_platform_update(self):
        """
        This method is used to test the platform update method.
        """
        # Test the update method
        for platform in self.platforms:
            platform.save(self.connection)
            platform.update(self.connection)
            # Assert that the platform objects are updated into the database.
            logger.debug(
                """Platform %s: '%s' updated in the database.""", platform.id, platform.name)
        logger.info('Platforms updated into the database.')

        # Assert that the platform objects throw an exception when the name is not found in the database.
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')
        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):
            platform.update(self.connection)

        logger.info('test_platform_update: PASS')

    def test_platform_save_platforms(self):
        """
        This method is used to test the platform save_platforms method.
        """
        # Test the save_platforms method
        Platform.save_platforms(self.platforms, self.connection)

        # Assert that the platform objects are saved into the database.
        for platform, i in zip(self.platforms, range(1, 4)):
            logger.debug("""-> %s.id=%s i=%s""", platform.name, platform.id, i)
            self.assertEqual(platform.id, i)

            logger.debug(
                """Platform %s: '%s' saved into the database.""", platform.id, platform.name)

        logger.info('Platforms saved in bulk into the database.')

        logger.info('test_platform_save_platforms: PASS')


if __name__ == '__main__':
    unittest.main()
