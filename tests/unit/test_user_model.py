"""Unit tests for the User model."""

# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    if str(project_directory) not in sys.path:
        sys.path.append(str(project_directory))

import unittest

from model.user_model import UserModel


class TestUserModel(unittest.TestCase):
    """This is the unit test class for the User model."""

    def setUp(self):
        """Set up the User model unit test."""
        self.user_model = UserModel()

    def test_user_model(self):
        """Test the User model."""
        self.assertIsInstance(self.user_model, UserModel)

        # Assert that the private properties are set to None
        self.assertIsNone(self.user_model.user_name)
        self.assertIsNone(self.user_model.full_name)

        # Assert that the public properties are set to the correct values
        user = self.user_model
        user.user_name = "test"
        user.full_name = "test full name"

        # Assert that the @property decorator works
        self.assertEqual(user.user_name, "test")
        self.assertEqual(user.full_name, "test full name")

        # Assert that the @property setter decorator works
        user.user_name = "test2"
        user.full_name = "test2 full name"

        self.assertEqual(user.user_name, "test2")
        self.assertEqual(user.full_name, "test2 full name")

        # Assert that the @property deleter decorator works
        del user.user_name
        del user.full_name

        self.assertIsNone(user.user_name)
        self.assertIsNone(user.full_name)

    def test_save(self):
        """Test the insert_user method."""
        user = self.user_model
        user.user_name = "test user name"
        user.full_name = "test full name"
        user.nick_name = "test nick name"

        expected = [(1, "test user name", "test full name", "test nick name")]

        # Assert that the insert_user method returns the correct value
        self.assertEqual(user.save(), expected)

        # Assert that the insert_user method throws an error when the user_name is None
        user.user_name = None
        with self.assertRaises(ValueError):
            user.save()
            user.logger.info("User name cannot be None")
            user.logger.debug("User name cannot be None")


if __name__ == "__main__":
    unittest.main()
