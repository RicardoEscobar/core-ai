"""
This data model is used to store the platform information of the user.
"""
from dataclasses import dataclass


@dataclass
class Platform:
    """
    This data model is used to store the `"user".platform` row data.
    """
    name: str
    description: str = None
    _id: int = None

    def __init__(self, _id: int, name: str, description: str):
        self._id = _id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Platform(_id={self._id}, name={self.name}, description={self.description})"

    def __str__(self):
        return f"""ROW({self._id}, $${self.name}$$, $${self.description}$$)::"user".platform"""

    def save(self):
        """
        This method is used to save the platform data into the database.
        """
        return self._id
