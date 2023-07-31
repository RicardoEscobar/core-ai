"""Unit tests for the code_filter module."""
if __name__ == "__main__":
    import sys
    import os

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.append(ROOT_DIR)

import unittest
from pathlib import Path
import logging

from controller.code_filter import CodeFilter
from controller.create_logger import create_logger

# Create logger
module_logger = create_logger(
    logger_name="tests.unit.test_code_filter",
    logger_filename="code_filter.log",
    log_directory="logs",
    add_date_to_filename=False,
)


class TestCodeFilter(unittest.TestCase):
    """Test the code_filter module."""

    def setUp(self) -> None:
        """Set up the test."""

        # Setup logging configuration.
        self.logger = module_logger

        # Create test file
        file_path = "tests/unit/markdown_test_file.md"
        self.test_file_path = Path(file_path)

        # Create file contents
        self.input_text = """Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero.

```python
def fibonacci(n):
    \"\"\"Generates the Fibonacci sequence up to n.\"\"\"
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

for num in fibonacci(100):
    print(num)
```

Este archivo es para probar el filtro de codigo."""

        # write test file
        with open(self.test_file_path, "w+", encoding="utf-8") as file:
            file.write(self.input_text)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test."""
        # delete test file
        self.test_file_path.unlink()

        return super().tearDown()

    def test_filtered_str(self):
        """Test the filtered_str and filtered_file_str properties."""

        self.logger.info("==========test_filtered_str==========")
        text = """Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero.

```python
def fibonacci(n):
    \"\"\"Generates the Fibonacci sequence up to n.\"\"\"
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

for num in fibonacci(100):
    print(num)
```"""

        code_filter = CodeFilter(text=text)
        expected_result = "Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero."
        actual_result = code_filter.filtered_str
        self.assertEqual(expected_result, actual_result)

    def test_filtered_file_str(self):
        """Test the filtered_str and filtered_file_str properties."""
        self.logger.info("==========test_filtered_file_str==========")

        # Test with a file path.
        file_path = str(self.test_file_path.resolve())
        self.logger.info(
            "First instance of file_path: %s on test_filtered_file_str", file_path
        )
        code_filter = CodeFilter(file_path=file_path)
        expected_result = "Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero.\nEste archivo es para probar el filtro de codigo."
        actual_result = code_filter.filtered_file_str
        self.assertEqual(expected_result, actual_result)

        # Assert that an exeption is raised if self.file_path is None, There is no file to read.
        self.logger.info("Second instance of CodeFilter without file_path or text")
        code_filter = CodeFilter()
        with self.assertRaises(ValueError):
            _ = code_filter.filtered_file_str


if __name__ == "__main__":
    unittest.main()
