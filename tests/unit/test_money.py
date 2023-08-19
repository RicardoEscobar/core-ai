"""Unit tests for the controller.money module."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import unittest

from controller.money import Money


class TestMoney(unittest.TestCase):
    """Unit tests for the controller.money module."""

    def test_init(self):
        """Test the Money class constructor."""
        money = Money(100_000, "MXN")
        self.assertEqual(money.amount, 100_000)
        self.assertEqual(money.currency, "MXN")

    def test_str(self):
        """Test the Money class __str__ method."""
        money = Money(100_000, "MXN")
        self.assertEqual(str(money), "$100,000.00 MXN")

    def test_repr(self):
        """Test the Money class __repr__ method."""
        money = Money(100_000, "MXN")
        self.assertEqual(repr(money), "Money(100000, 'MXN')")

    def test_cents_to_currency_unit(self):
        """Test the Money class cents_to_currency_unit method."""

        # Assert cents to currency unit conversion
        self.assertEqual(Money.cents_to_currency_unit(100000), 1000.00)
        self.assertEqual(Money.cents_to_currency_unit(100_000_000), 1000000.00)
        self.assertEqual(Money.cents_to_currency_unit(100_000_000_000), 1000000000.00)

        # Assert type error when setting amount with non-numeric value
        with self.assertRaises(TypeError):
            Money.cents_to_currency_unit("100000")

    def test_currency_unit_to_cents(self):
        """Test the Money class currency_unit_to_cents method."""

        self.assertEqual(Money.currency_unit_to_cents(1000), 100000)
        self.assertEqual(Money.currency_unit_to_cents(1000000.00), 100_000_000)
        self.assertEqual(Money.currency_unit_to_cents(1000000000.00), 100_000_000_000)

        # Assert type error when setting amount with non-numeric value
        with self.assertRaises(TypeError):
            Money.currency_unit_to_cents("1000")

    def test_cents_property(self):
        """Test the Money class cents property."""
        money = Money(100_000, "MXN")

        # Assert cents property
        self.assertEqual(money.cents, 10000000)

        # Assert cents setter
        money.cents = 500
        self.assertEqual(money.amount, 5)
        self.assertEqual(money.cents, 500)

        # Assert cents setter with negative value
        money.cents = -500
        self.assertEqual(money.amount, -5)
        self.assertEqual(money.cents, -500)

        # Assert cents setter with zero value
        money.cents = 0
        self.assertEqual(money.amount, 0)
        self.assertEqual(money.cents, 0)

        # Assert cents deleter
        del money.cents
        self.assertEqual(money.amount, 0)
        self.assertEqual(money.cents, 0)

        # Assert type error when setting cents with non-integer value
        with self.assertRaises(TypeError):
            money.cents = "500"


if __name__ == "__main__":
    unittest.main()
