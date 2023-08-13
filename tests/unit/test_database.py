"""
This module contains the unit tests for the database module.
"""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os
import unittest
import logging
from unittest.mock import patch, mock_open
import pdb

import psycopg

from dotenv import load_dotenv
from model.database import Database
from controller.create_logger import create_logger

# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_database",
    logger_filename="test_database.log",
    log_directory="logs/tests",
    console_logging=False,
    console_log_level=logging.INFO,
)


class TestDatabase(unittest.TestCase):
    """This class contains the unit tests for the database module."""

    @classmethod
    def setUpClass(cls):
        # Create class logger instance
        cls.logger = module_logger
        cls.logger.info("===Testing database module===")

        # load the environment variables
        load_dotenv()

        # Connect to an existing database
        cls.connection = psycopg.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
        )

    @classmethod
    def tearDownClass(cls):
        cls.logger.info("===Finished testing database module===")

        # Clean up environment variables
        del os.environ["DB_NAME"]
        del os.environ["DB_USER"]
        del os.environ["DB_PASSWORD"]
        del os.environ["DB_HOST"]
        del os.environ["DB_PORT"]

    def setUp(self):
        # Create a new database instance for each test
        self.db = Database()

    def tearDown(self):
        self.logger.info("Tearing down database test")
        # Delete inserted user records after each test
        cursor = self.connection.cursor()
        cursor.execute('TRUNCATE TABLE public."user" CASCADE;')
        cursor.connection.commit()

        # Close the database connection after each test
        del self.db

    def test_execute(self):
        """Test the execute method"""
        result = self.db.execute("SELECT 1")
        self.assertEqual(result, [(1,)])

    def test_execute_with_values(self):
        """Test the execute method with values"""
        result = self.db.execute("SELECT %s", (1,))
        self.assertEqual(result, [(1,)])

    def test_execute_with_insert(self):
        """Test the execute method with an insert statement"""
        self.logger.info("Testing execute method with an insert statement")
        query = 'INSERT INTO public."user"(id, name, full_name)	VALUES (%s, %s, %s) RETURNING id, name, full_name;;'
        values = (1, "AnimArt3d", "AnimArt3d twitch viewer")
        expected_result = [(1, "AnimArt3d", "AnimArt3d twitch viewer")]

        # Create a mock cursor with a context manager
        with patch('psycopg.Cursor.execute') as mock_execute:
            with patch('psycopg.Cursor.fetchall', return_value=expected_result) as mock_fetchall:
                actual_result = self.db.execute(query, values)
                mock_execute.assert_called_once_with(query, values)
                mock_fetchall.assert_called_once()
                self.assertEqual(actual_result, expected_result)

    def test_execute_many(self):
        """Test the execute_many method"""
        result = self.db.execute_many("SELECT %s", [(1,), (2,), (3,)])
        self.assertEqual(result, [(1,), (2,), (3,)])

    def test_execute_script(self):
        """Test the execute_script method"""
        result = self.db.execute_script("SELECT 1")
        self.assertEqual(result, [(1,)])

    @patch("builtins.open", new_callable=mock_open, read_data="SELECT 1")
    def test_execute_script_file(self, mock_file):
        """Test the execute_script_file method"""
        result = self.db.execute_script_file(
            "databases/core_ai/tables/user_platform.sql"
        )
        self.assertEqual(result, [(1,)])
        mock_file.assert_called_once_with(
            "databases/core_ai/tables/user_platform.sql", "r", encoding="utf-8"
        )

    @unittest.skip("TODO - implement DELETE user table test")
    def test_delete_user_table(self):
        """Test the delete_user_table method"""
        pass

    @unittest.skip("TODO - implement UPDATE user table test")
    def test_update_user_table(self):
        """Test the update_user_table method"""
        pass


if __name__ == "__main__":
    unittest.main()
