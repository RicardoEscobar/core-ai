"""
Unit tests for the platform module.
"""
import os
import unittest
import psycopg
from dotenv import load_dotenv
from model.user.platform import Platform


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
);

COMMENT ON TABLE "user".platform
    IS 'Platform information, where the user is interacting with the AI.
The same user may create several accounts on the same or different platforms.';

COMMENT ON COLUMN "user".platform.name
    IS 'text
Required
Name of the platform.';

COMMENT ON COLUMN "user".platform.description
    IS 'text
Optional
Description of the platform.';

-- Reset the sequence.
SELECT setval(pg_get_serial_sequence('"user".platform', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "user".platform;
"""
        cls.TRUNCATE_TABLE = """TRUNCATE TABLE "user".platform CASCADE;"""

        # Open a cursor to perform database operations
        with cls.connection.cursor() as cursor:
            cursor.execute(cls.DROP_TABLE)
            cursor.execute(cls.CREATE_TABLE)
            # cursor.execute(TRUNCATE_TABLE)
            cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        """
        This method is used to tear down the test environment.
        """

        with cls.connection.cursor() as cursor:
            cursor.execute(cls.DROP_TABLE)
            cursor.execute(cls.CREATE_TABLE)

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

    def test_platform_get_id(self):
        """
        This method is used to test the platform get_id method.
        """
        # Test the get_id method
        for expected_id, platform in enumerate(self.platforms, start=1):
            platform.save(self.connection)
            # Get id's from the database
            platform_id = platform.get_id(self.connection)
            # Assert that the platform objects got their id's from the database.
            self.assertEqual(platform_id, expected_id)

        # Assert that the platform objects trhow an exception when the name is not found in the database.
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')

        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):
            platform.get_id(self.connection)


if __name__ == '__main__':
    unittest.main()
