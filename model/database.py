"""
This database module is used to connect to the database and perform database operations.
"""
import os
import logging
import psycopg
from dotenv import load_dotenv
from controller.create_logger import create_logger

module_logger = create_logger(
    logger_name='model.database',
    logger_filename='database.log',
    log_directory='logs/database'
)


class Database():
    """
    This class is used to connect to the database and perform database operations.
    """

    def __init__(self):
        """
        This method is used to initialize the database connection.
        """
        self.logger = logging.getLogger('model.database.Database')
        self.logger.info('Creating an instance of Database')

        # load the environment variables
        load_dotenv()

        # Connect to an existing database
        self.connection = psycopg.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT')
        )

    def __del__(self):
        """
        This method is used to close the database connection.
        """
        self.logger.info('Closing the database connection.')
        # Close the connection
        self.connection.close()

    def execute(self, query: str, values: tuple = None) -> list:
        """
        This method is used to execute a query on the database.
        """
        self.logger.info('Executing query: %s', query)
        # Open a cursor to perform database operations
        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.fetchall()

    def execute_many(self, query: str, values: list) -> list:
        """
        This method is used to execute a query on the database.
        """
        self.logger.info('Executing query: %s', query)
        # Open a cursor to perform database operations
        with self.connection.cursor() as cursor:
            cursor.executemany(query, params_seq=values, returning=True)
            self.connection.commit()

            # Fetch all the rows
            resultset = []
            for row in cursor:
                resultset.append(row)
                module_logger.debug("row=%s", row)
                cursor.nextset()

            return resultset

    def execute_script(self, script: str) -> list:
        """
        This method is used to execute a script on the database.
        """
        self.logger.info('Executing script: %s', script)
        # Open a cursor to perform database operations
        with self.connection.cursor() as cursor:
            cursor.execute(script)
            self.connection.commit()
            return cursor.fetchall()

    def execute_script_file(self, file_path: str) -> list:
        """
        This method is used to execute a script on the database.
        """
        self.logger.info('Executing script file: %s', file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            script = file.read()
        return self.execute_script(script)
