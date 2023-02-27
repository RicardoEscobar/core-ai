import os
import unittest
from unittest.mock import patch, Mock, mock_open
import model.database
from model.database import Database
from dotenv import load_dotenv
import psycopg


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # load the environment variables
        load_dotenv()

        # Connect to an existing database
        cls.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

    @classmethod
    def tearDownClass(cls):
        # Clean up environment variables
        del os.environ['DB_NAME']
        del os.environ['DB_USER']
        del os.environ['DB_PASSWORD']
        del os.environ['DB_HOST']
        del os.environ['DB_PORT']

    def setUp(self):
        # Create a new database instance for each test
        self.db = Database()

    def tearDown(self):
        # Close the database connection after each test
        del self.db

    def test_execute(self):
        # Test the execute method
        result = self.db.execute('SELECT 1')
        self.assertEqual(result, [(1,)])

    def test_execute_with_values(self):
        # Test the execute method with values
        result = self.db.execute('SELECT %s', (1,))
        self.assertEqual(result, [(1,)])

    def test_execute_many(self):
        # Test the execute_many method
        result = self.db.execute_many('SELECT %s', [(1,), (2,), (3,)])
        self.assertEqual(result, [(1,), (2,), (3,)])

    def test_execute_script(self):
        # Test the execute_script method
        result = self.db.execute_script('SELECT 1')
        self.assertEqual(result, [(1,)])

    @patch('builtins.open', new_callable=mock_open, read_data='SELECT 1')
    def test_execute_script_file(self, mock_file):
        # Test the execute_script_file method
        result = self.db.execute_script_file(
            'databases/core_ai/tables/user_platform.sql')
        self.assertEqual(result, [(1,)])
        mock_file.assert_called_once_with(
            'databases/core_ai/tables/user_platform.sql', 'r')


if __name__ == '__main__':
    unittest.main()
