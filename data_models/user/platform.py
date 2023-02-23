"""
This data model is used to store the platform information of the user.
"""
from dataclasses import dataclass
import psycopg
from typing import List


@dataclass
class Platform:
    """
    This data model is used to store the `"user".platform` row data.
    """
    name: str
    description: str = None
    _id: int = None
    table_name: str = '"user".platform'

    def __init__(self, name: str, description: str = None, _id: int = None):
        self._id = _id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Platform(_id={self._id}, name={self.name!r}, description={self.description!r})"

    def __str__(self):
        return f"""({self._id if self._id else 'DEFAULT'}, $${self.name}$$, $${self.description}$$)"""

    def as_tuple(self):
        return (self._id if self._id else 'DEFAULT', self.name, self.description)

    def get_id(self, connection: psycopg.connection = None):
        """
        This method is used to get the id of the platform.
        """
        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""SELECT id FROM {Platform.table_name} WHERE name = $${self.name}$$;"""
                cursor.execute(query)
                first_row = cursor.fetchone()

                # set the _id of the object
                self._id = first_row[0]
                return self._id

    def save(self, connection: psycopg.connection = None):
        """
        This method is used to save the platform data into the database.
        """
        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""INSERT INTO {Platform.table_name} VALUES {self} ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description RETURNING *;"""
                cursor.execute(query)
                connection.commit()
                first_row = cursor.fetchone()

                # set the _id of the object
                self._id = first_row[0]

    @classmethod
    def save_platforms(cls, platforms: List["Platform"], connection: psycopg.connection = None):
        """
        This method is used to save the platform data into the database. From a list of Platform objects.
        Here is the explanation for the code:
        1. The "Platform" data model is used to store the platform data of the user.
        2. The "get_id" method is used to get the id of the platform.
        3. The "save" method is used to save the platform data into the database.
        4. The "save_platforms" method is used to save a list of platform objects into the database.
        """
        # Convert the list of Platform objects into a tuple of tuples
        platforms_tuples = (platform.as_tuple() for platform in platforms)

        if connection:
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                query = f"""INSERT INTO {Platform.table_name} VALUES %s ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description RETURNING *;"""
                print(query)
                cursor.executemany(
                    query, params_seq=platforms_tuples, returning=True)

                connection.commit()
                all_rows = cursor.fetchall()

                # set the _id of the object
                for row in all_rows:
                    platforms[all_rows.index(row)]._id = row['id']
