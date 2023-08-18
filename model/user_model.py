# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    if str(root_folder) not in sys.path:
        sys.path.append(str(root_folder))

import logging
from typing import List, Tuple

from model.database import Database
from controller.create_logger import create_logger

module_logger = create_logger(
    logger_name="model.user_model",
    logger_filename="user_model.log",
    log_directory="logs/database",
    add_date_to_filename=False,
    console_logging=False,
    console_log_level=logging.INFO,
)

# Load the environment variables
# load_dotenv()

class UserModel(Database):
    """This class represents the user model. this model is for inserting,
    updating, deleting, and selecting user data from the postgresql database"""

    def __init__(
        self,
        user_name: str = None,
        full_name: str = None,
        nick_name: str = None,
    ):
        """This method is used to initialize the user model."""
        super().__init__()

        # Override the logger, execute after super().__init__() or else the logger will be overwritten by the super().__init__() method
        self.logger = module_logger

        # Private properties
        self._id = None
        self._user_name = user_name
        self._full_name = full_name
        self._nick_name = nick_name

    @property
    def user_name(self) -> str:
        """This method is a getter for the name property."""
        return self._user_name

    @user_name.setter
    def user_name(self, name: str) -> None:
        """This method is a setter for the name property."""
        self._user_name = name

    @user_name.deleter
    def user_name(self) -> None:
        """This method is a deleter for the name property."""
        self._user_name = None

    @property
    def full_name(self) -> str:
        """This method is a getter for the full_name property."""
        return self._full_name

    @full_name.setter
    def full_name(self, full_name: str) -> None:
        """This method is a setter for the full_name property."""
        self._full_name = full_name

    @full_name.deleter
    def full_name(self) -> None:
        """This method is a deleter for the full_name property."""
        self._full_name = None

    @property
    def nick_name(self) -> str:
        """This method is a getter for the nick_name property."""
        return self._nick_name

    @nick_name.setter
    def nick_name(self, nick_name: str) -> None:
        """This method is a setter for the nick_name property."""
        self._nick_name = nick_name

    @nick_name.deleter
    def nick_name(self) -> None:
        """This method is a deleter for the nick_name property."""
        self._nick_name = None

    def save(self) -> List[Tuple]:
        """This method is used to insert a user into the database."""
        if self.user_name is None:
            raise ValueError("The user_name property cannot be None")

        self.logger.debug(
            "Inserting user: %s, %s, %s",
            repr(self.user_name),
            repr(self.full_name),
            repr(self.nick_name),
        )

        insert_user_query = """
    INSERT INTO public."user" (user_name, full_name, nick_name)
    VALUES (%s, %s, %s)
    ON CONFLICT (user_name) DO UPDATE SET full_name = EXCLUDED.full_name, nick_name = EXCLUDED.nick_name
    RETURNING id, user_name, full_name, nick_name
"""
        values = (self.user_name, self.full_name, self.nick_name)

        # Insert the user into the database
        result = self.execute(insert_user_query, values)
        self.logger.debug("Inserted row at public.user: %s", result)

        # Assign the id to the user object
        self._id = result[0][0]

        return result


if __name__ == "__main__":
    user_model = UserModel()
    print(user_model)
