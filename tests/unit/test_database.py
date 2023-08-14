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
import datetime
import pytz

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
        """Set up the database test"""
        # Create class logger instance
        cls.logger = module_logger
        cls.logger.info("===Testing database module===")

        # Create user timezone
        cls.user_timezone = pytz.timezone("America/Mexico_City")
        cls.user_timezone_localized = cls.user_timezone.localize(datetime.datetime.now())
        cls.user_utc_datetime = cls.user_timezone_localized.astimezone(pytz.utc)

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
        """Tear down the database test"""
        cls.logger.info("===Finished testing database module===")

        # Clean up environment variables
        del os.environ["DB_NAME"]
        del os.environ["DB_USER"]
        del os.environ["DB_PASSWORD"]
        del os.environ["DB_HOST"]
        del os.environ["DB_PORT"]

        # Close the database connection after each test
        cls.connection.close()

    def setUp(self):
        """Set up the database test"""
        # Create a new database instance for each test
        self.db = Database()

        # Create a test table in the database to test INSERTS, UPDATES, and DELETES
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS public.test_table (
                    id serial PRIMARY KEY,
                    name text,
                    email text,
                    date_of_birth date,
                    rank integer,
                    salary money DEFAULT 6970.0);
                """
            )
            self.connection.commit()

    def tearDown(self):
        """Tear down the database test"""
        # Delete inserted user records after each test
        self.logger.info("Tearing down database test")
        cursor = self.connection.cursor()
        cursor.execute('TRUNCATE TABLE public."user" CASCADE;')
        cursor.connection.commit()

        # Drop test table in the database
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE public.test_table CASCADE;")
            self.connection.commit()
            if cursor.rowcount == 0:
                self.logger.info("Dropped test table in the database")
            else:
                self.logger.error("Failed to drop test table in the database")

    def test_execute(self):
        """Test the execute method"""
        expected = [(1,)]

        # Create a mock cursor with a context manager
        with patch("psycopg.Cursor.execute") as mock_execute:
            with patch(
                "psycopg.Cursor.fetchall", return_value=expected
            ) as mock_fetchall:
                result = self.db.execute("SELECT 1")
                mock_execute.assert_called_once_with("SELECT 1", None)
                mock_fetchall.assert_called_once()
                self.assertEqual(result, expected)

    def test_execute_with_values(self):
        """Test the execute method with values"""
        values = (1,)
        expected = [(1,)]

        # Create a mock cursor with a context manager
        with patch("psycopg.Cursor.execute") as mock_execute:
            with patch(
                "psycopg.Cursor.fetchall", return_value=expected
            ) as mock_fetchall:
                result = self.db.execute("SELECT %s", values)
                mock_execute.assert_called_once_with("SELECT %s", values)
                mock_fetchall.assert_called_once()
                self.assertEqual(result, expected)

    def test_execute_many(self):
        """Test the execute_many method"""
        values = [(1,), (2,), (3,)]
        expected = [(1,), (2,), (3,)]

        # Create a mock cursor with a context manager
        with patch("psycopg.Cursor.executemany") as mock_executemany:
            with patch(
                "psycopg.Cursor.fetchall", return_value=expected
            ) as mock_fetchall:
                result = self.db.execute_many("SELECT %s", values)
                mock_executemany.assert_called_once_with(
                    "SELECT %s", params_seq=values, returning=True
                )
                mock_fetchall.assert_called_once()
                self.assertEqual(result, expected)

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

    def test_execute_with_insert(self):
        """Test the execute method with an insert statement on public.user table"""
        self.logger.info("Testing execute method with an insert statement")
        date_of_birth = psycopg.Date(1990, 1, 1)
        salary = "6970::money"
        query = """
            INSERT INTO public.test_table
                (name, email, date_of_birth, rank, salary)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, email, date_of_birth, rank, salary;
        """
        values = ("AnimArt3d", "animart3d@gmail.com", date_of_birth, 1, salary)
        expected_result = [(1, "AnimArt3d", "animart3d@gmail.com", "1990-01-01", 1, 6970.0)]

        # Create a mock cursor with a context manager
        # with patch("psycopg.Cursor.execute") as mock_execute:
        #     with patch(
        #         "psycopg.Cursor.fetchall", return_value=expected_result
        #     ) as mock_fetchall:
        #         actual_result = self.db.execute(query, values)
        #         mock_execute.assert_called_once_with(query, values)
        #         mock_fetchall.assert_called_once()
        actual_result = self.db.execute(query, values)
        self.assertEqual(actual_result, expected_result)

    @unittest.skip("TODO - implement DELETE user table test")
    def test_execute_delete_one_row(self):
        """Test the delete a single row from given a table"""
        pass

    @unittest.skip("TODO - implement UPDATE user table test")
    def test_update_user_table(self):
        """Test the update_user_table method"""
        pass


if __name__ == "__main__":
    unittest.main()
