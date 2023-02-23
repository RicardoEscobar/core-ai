"""
This data model is used to store the platform information of the user.
"""
from dataclasses import dataclass
import psycopg


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
        return f"Platform(_id={self._id}, name={self.name}, description={self.description})"

    def __str__(self):
        return f"""({self._id if self._id else 'DEFAULT'}, $${self.name}$$, $${self.description}$$)"""

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
                query = f"""INSERT INTO {Platform.table_name} VALUES {self} ON RETURNING *;"""
                try:
                    cursor.execute(query)
                except psycopg.errors.UniqueViolation:
                    print(
                        f"Platform {self.name} already exists in the database.")
                    self._id = self.get_id(connection)
                connection.commit()
                first_row = cursor.fetchone()

                # set the _id of the object
                self._id = first_row[0]

    # Define _id as a property
    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, _id: int):
        self.__id = _id

    @_id.deleter
    def _id(self):
        del self.__id
