"""Unit tests for the code_filter module."""
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import unittest
from controller.code_filter import CodeFilter


class TestCodeFilter(unittest.TestCase):
    """Test the chat module."""

    def test_filter_code_block(self):
        """Test the filter_code_block method."""

        input_text = """Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero.

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
        code_filter = CodeFilter(input_text)
        expected_result = "Si Ricardo aqui esta el codigo para hacer una funcion generador en Python que entregue los numeros de la serie fibonacci dando un numero."
        actual_result = code_filter.filter_code_block()
        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
