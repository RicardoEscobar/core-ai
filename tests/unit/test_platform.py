"""
Unit tests for the platform module.
"""
import os
import unittest
from unittest.mock import patch
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

        # Connect to an existing database.
        cls.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

        # Create a mock connection and cursor.
        cls.mock_connect = patch('psycopg.connect').start()
        cls.mock_connection = cls.mock_connect.return_value
        cls.mock_cursor = cls.mock_connection.cursor.return_value

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
        cls.INSERT_DATA = """INSERT INTO "user".platform (name, description)
VALUES
('Core AI','Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.'),
('VRChat','VRChat is a social VR platform where users can create and share their own virtual worlds, avatars, and experiences.')
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description
RETURNING *;"""

    @classmethod
    def tearDownClass(cls):
        """
        This method is used to tear down the test environment.
        """
        # Close the connection
        cls.connection.close()

    def setUp(self):
        """
        This method is used to set up the test environment.
        """
        # Set the connection and mock connect, mock connection, and mock cursor.
        self.connection = self.__class__.connection
        self.mock_connect = self.__class__.mock_connect
        self.mock_connection = self.__class__.mock_connection
        self.mock_cursor = self.__class__.mock_cursor

        # Create Platform objects
        self.core_ai = Platform(
            name='Core AI', description="""Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.""")
        self.vrchat = Platform(
            name='VRChat', description='VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.')
        self.twitch = Platform(
            name='Twitch', description='Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.')

        # Save the platform objects into a list
        self.platforms = [self.core_ai,  self.vrchat,  self.twitch]

        # Open a cursor to perform database operations
        with patch('psycopg.Connection') as mock_connection:
            with patch('psycopg.cursor.Cursor') as mock_cursor:
                mock_cursor.execute(self.DROP_TABLE)
                mock_cursor.execute(self.CREATE_TABLE)
                mock_cursor.execute(self.RESET_SEQUENCE)
                mock_cursor.execute(self.INSERT_DATA)
                # mock_cursor.execute(TRUNCATE_TABLE)
                mock_connection.commit()

    def test_platform_str_repr(self):
        """
        This method is used to test the platform data model.
        """

        # Create expected values.
        expected = """(DEFAULT, $$Core AI$$, $$Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.$$)"""

        # Assert the __str__ method
        self.assertEqual(str(self.core_ai), expected)

        # Assert the __repr__ method
        expected = """Platform(_id=None, name='Core AI', description='Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.')"""
        self.assertEqual(repr(self.core_ai), expected)

    def test_platform_save(self):
        """
        This method is used to test the platform save method.
        """
        # Create expected values.
        expected = tuple([
            (1, 'Core AI', """Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters."""),
            (2, 'VRChat', 'VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.'),
            (3, 'Twitch', 'Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.')
        ])

        # Test the save method
        for i, platform in enumerate(self.platforms, start=1):

            # Mock the fetchone method to return the expected row's.
            # Compensate for the 0 index: expected[i-1].
            self.mock_cursor.__enter__.return_value.fetchone.return_value = expected[i-1]

            platform.save(self.mock_connection)
            # Assert that the platform objects are saved into the database.
            self.assertEqual(platform.id, i)

        # Assert that the platform objects are updated into the database when there is a conflict on the name column.
        expected = """Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon, and it's great!"""

        # Mock the fetchone method to return the expected row's.
        self.mock_cursor.__enter__.return_value.fetchone.return_value = (
            3, 'Twitch', expected)

        platform_updated = Platform('Twitch', expected)
        platform_updated.save(self.mock_connection)
        self.assertEqual(platform_updated.description, expected)

    def test_platform_load(self):
        """
        This method is used to test the platform load method.
        """
        expected = (
            1, 'Core AI', 'Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.')

        # Mock the fetchone method to return the expected row's.
        self.mock_cursor.__enter__.return_value.fetchone.return_value = expected

        # Get id's from the database.
        result = self.core_ai.load(self.mock_connection)

        # Assert that the platform objects got their id's from the database.
        self.assertEqual(result, self.core_ai.id)

        # Assert that the platform objects trhow an exception when the name is not found in the database.
        expected = None
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')
        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):

            # Create a mock fetchone method.
            self.mock_cursor.__enter__.return_value.fetchone.return_value = expected

            # Call the load method.
            platform.load(self.mock_connection)

    def test_platform_delete(self):
        """
        This method is used to test the platform delete method.
        """
        # Create expected values.
        expected = tuple([
            (1, 'Core AI', """Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters."""),
            (2, 'VRChat', 'VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.'),
            (3, 'Twitch', 'Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.')
        ])

        # Test the delete method.
        for i, platform in enumerate(self.platforms, start=1):
            # Set id's for the platform objects.
            platform.id = i

            # Create a mock fetchone method.
            # Compensate for the 0 index: expected[i-1].
            self.mock_cursor.__enter__.return_value.fetchone.return_value = expected[i-1]

            platform.delete(self.mock_connection)
            # Assert that the platform objects are deleted from the database.
            self.assertIsNone(platform.id)

        # Assert that the platform objects throw an exception when the name is not found in the database.
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')

        # Create a mock fetchone method.
        self.mock_cursor.__enter__.return_value.fetchone.return_value = None

        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):
            platform.delete(self.mock_connection)

    def test_platform_update(self):
        """
        This method is used to test the platform update method.
        """
        # Create expected values.
        expected = tuple([
            (1, 'Core AI', """UPDATED: Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters."""),
            (2, 'VRChat', 'UPDATED: VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.'),
            (3, 'Twitch', 'UPDATED: Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.')
        ])

        # Test the update method.
        for i, platform in enumerate(self.platforms, start=1):
            # Create a mock fetchone method.
            # Compensate for the 0 index: expected[i-1].
            self.mock_cursor.__enter__.return_value.fetchone.return_value = expected[i-1]

            platform.update(self.mock_connection)

            # Assert that the platform objects are updated into the database.
            self.assertEqual(platform.description, expected[i-1][2])

        # Assert that the platform objects throw an exception when the name is not found in the database.
        platform = Platform(
            'Facebook', 'Facebook is a social networking service.')

        # Create a mock fetchone method.
        self.mock_cursor.__enter__.return_value.fetchone.return_value = None

        with self.assertRaises(ValueError, msg=f"""Platform '{platform.name}' does not exist in the database. Please use save the platform first."""):
            platform.update(self.mock_connection)

    def test_platform_save_platforms(self):
        """
        This method is used to test the platform save_platforms method.
        """

        # Create expected returned row values.
        mock_resultset = (
            (1, 'Core AI', 'Core AI is a platform for interacting with AI powered chatbots, NPCs, and other virtual characters.'),
            (2, 'VRChat', 'VRChat is a massively multiplayer online virtual reality social platform developed and published by VRChat Inc.'),
            (3, 'Twitch', 'Twitch is a live streaming video platform owned by Twitch Interactive, a subsidiary of Amazon.')
        )

        # Create a mock cursor.__iter__() method.
        self.mock_cursor.__enter__.return_value.__iter__.return_value = mock_resultset

        # Call the save_platforms method.
        Platform.save_platforms(self.platforms, self.mock_connection)

        # Assert that the platform objects are saved into the database.
        self.assertEqual(self.platforms[0].id, mock_resultset[0][0])
        self.assertEqual(self.platforms[1].id, mock_resultset[1][0])
        self.assertEqual(self.platforms[2].id, mock_resultset[2][0])


if __name__ == '__main__':
    unittest.main()
