"""Unit tests for ask_database.py"""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import unittest


class TestAskDatabase(unittest.TestCase):
    """Test case for ask_database.py"""

    def test_get_table_names(self):
        """Test get_table_names()"""
        pass