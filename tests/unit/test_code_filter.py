"""Unit tests for the code_filter module."""
if __name__ == "__main__":
    import sys
    import os

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

import unittest
from pathlib import Path

from controller.code_filter import CodeFilter


class TestCodeFilter(unittest.TestCase):
    """Test the chat module."""

    def setUp(self) -> None:
        """Set up the test."""

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

        # Test with a file path.
        file_path = str(self.test_file_path.resolve())
        code_filter = CodeFilter(file_path=file_path)
        expected_result = "Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero.\nEste archivo es para probar el filtro de codigo."
        actual_result = code_filter.filtered_file_str
        self.assertEqual(expected_result, actual_result)



if __name__ == "__main__":
    unittest.main()
