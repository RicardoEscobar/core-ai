"""
This data model is used to store the platform information of the user.
"""

import logging
from dataclasses import dataclass
from typing import List, Tuple, Union
import psycopg
from controller.create_logger import create_logger


module_logger = create_logger(
    logger_name='model.user.platform',
    logger_filename='platform.log',
    log_directory='logs/platform'
)


@dataclass
class Platform:
    """
    This data model is used to store the `"user".platform` row data.
    """
    name: str
    description: str = None
    _id: int = None
    table_name: str = '"user".platform'

    # getting the values
    @property
    def id(self):
        return self._id

    # setting the values
    @id.setter
    def id(self, id):
        self._id = id

    # deleting the values
    @id.deleter
    def id(self):
        del self._id

    def __init__(self, name: str, description: str = None, id: int = None):
        self.logger = logging.getLogger('model.user.platform.Platform')
        self.name = name
        self.description = description
        self.id = id
        self.logger.info(
            'Creating an instance of Platform(name=%s, description=%s, id=%s)', repr(name), repr(description), id)

    def __repr__(self):
        return f"Platform(_id={self._id}, name={self.name!r}, description={self.description!r})"

    def __str__(self):
        return f"""({self._id if self._id else 'DEFAULT'}, $${self.name}$$, $${self.description}$$)"""

    def load(self, connection: psycopg.connection = None) -> int:
        """
        This method is used to return the id of the platform and load the name and description of the platform.
        """
        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""SELECT * FROM {Platform.table_name} WHERE name = $${self.name}$$;"""
                module_logger.debug(
                    "Loading '%s' id from the database.", self.name)
                cursor.execute(query)
                first_row = cursor.fetchone()
                module_logger.debug("Loaded database row = %s", first_row)

                # set the _id of the object
                if first_row:
                    self.id = first_row[0]
                    self.name = first_row[1]
                    self.description = first_row[2]
                    module_logger.info(
                        "Loaded Platform(id=%s, name=%s, description=%s)", self.id, repr(self.name), repr(self.description))
                    return first_row[0]

                # if the platform does not exist in the database, raise an error. Else is unnecessary.
                module_logger.error(
                    "Platform '%s' does not exist in the database.", self.name)
                raise ValueError(
                    f"""Platform '{self.name}' does not exist in the database. Please use save the platform first.""")

    def save(self, connection: psycopg.connection = None) -> None:
        """
        This method is used to save the platform data into the database.
        """
        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""INSERT INTO {Platform.table_name} (id, name, description) VALUES (DEFAULT, %s, %s) ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description RETURNING *;"""
                cursor.execute(
                    query, (self.name, self.description))
                connection.commit()
                first_row = cursor.fetchone()

                # set the _id of the object
                self.id = first_row[0]
                self.name = first_row[1]
                self.description = first_row[2]
                module_logger.debug("Saved database row = %s", str(self))

    def delete(self, connection: psycopg.connection = None) -> None:
        """
        This method is used to delete the platform data from the database.
        """
        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""DELETE FROM {Platform.table_name} WHERE id = %s RETURNING *;"""
                cursor.execute(query, (self.id,))
                connection.commit()
                first_row = cursor.fetchone()

                if first_row:
                    module_logger.debug("Deleted database row = %s", str(self))
                    self.id = None
                else:
                    # if the platform does not exist in the database, raise an error. Else is unnecessary.
                    module_logger.error(
                        "Platform '%s' does not exist in the database.", self.name)
                    raise ValueError(
                        f"""Platform '{self.name}' does not exist in the database.""")

    def update(self, connection: psycopg.connection = None) -> None:
        """
        This method is used to update the platform data from the database.
        """
        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""UPDATE {Platform.table_name} SET name = %s, description = %s WHERE id = %s RETURNING *;"""
                cursor.execute(query, (self.name, self.description, self.id))
                connection.commit()
                first_row = cursor.fetchone()

                if first_row:
                    self.id = first_row[0]
                else:
                    raise ValueError(
                        f"""Platform '{self.name}' does not exist in the database.""")

    @classmethod
    def save_platforms(cls, platforms: Union[Tuple["Platform"], List["Platform"]], connection: psycopg.connection = None):
        """
        This method is used to save the platform data into the database. From a list of Platform objects.
        Here is the explanation for the code:
        1. The "Platform" data model is used to store the platform data of the user.
        2. The "get_id" method is used to get the id of the platform.
        3. The "save" method is used to save the platform data into the database.
        4. The "save_platforms" method is used to save a list of platform objects into the database.
        """
        # Convert the list of Platform objects into a tuple of tuples
        # make a list comprehension to get the tuple of each object, extract only name and description.
        params_seq = tuple((platform.name, platform.description)
                           for platform in platforms)
        module_logger.debug("params_seq=%s", params_seq)

        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""INSERT INTO {Platform.table_name} VALUES (DEFAULT, %s, %s) ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description RETURNING *;"""

                cursor.executemany(
                    query, params_seq=params_seq, returning=True)

                connection.commit()

                # Fetch all the rows
                for row in cursor:
                    # module_logger.debug("row=%s", row)
                    platforms[params_seq.index(row[1:])].id = row[0]
                    module_logger.debug(
                        "row=%s", platforms[params_seq.index(row[1:])])
                    cursor.nextset()
