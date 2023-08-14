"""This is a utility module to make operations with money, currencies and convert them between cents and whole numbers. This is meant to be used to store money values in a postgresql database as integers."""

from decimal import Decimal
from typing import Union
import locale


class Money:
    """A class to represent money values and convert them between cents and whole numbers."""

    def __init__(
        self,
        amount: Union[int, float, Decimal] = 0,
        currency: str = "USD"
    ) -> None:
        self.amount = amount
        self.currency = currency

    @staticmethod
    def cents_to_currency_unit(cents: int) -> Decimal:
        """
        Convert an integer representing cents into a Decimal amount.

        Args:
            cents (int): The integer value representing cents.

        Returns:
            Decimal: The corresponding amount in Decimal format.
        """
        dollars = cents // 100
        cents_remaining = cents % 100
        amount = Decimal(f"{dollars}.{cents_remaining:02}")
        return amount

    @staticmethod
    def currency_unit_to_cents(amount: Decimal) -> int:
        """
        Convert a Decimal amount to an integer representing cents.

        Args:
            amount (Decimal): The Decimal amount to convert.

        Returns:
            int: The equivalent integer value in cents.
        """
        cents = int(amount * 100)
        return cents

    @property
    def cents(self) -> int:
        """Return the amount in cents."""
        return self.currency_unit_to_cents(self.amount)
    
    @cents.setter
    def cents(self, cents: int) -> None:
        """Set the amount in cents."""
        self.amount = self.cents_to_currency_unit(cents)

    @cents.deleter
    def cents(self) -> None:
        """Delete the amount in cents."""
        del self.amount

    def __str__(self) -> str:
        """Return the amount as a string."""
        return f"{self.amount:.2f}"

    def __repr__(self) -> str:
        """Return the amount as a string."""
        return f"Money({self.amount}, '{self.currency}')"


if __name__ == "__main__":
    # Example usage
    money = Money()
    money.cents = 123_45 # 12345
    print(money)
    print(money.cents)

    # Set the desired locale (e.g., en_US for US English)
    locale.setlocale(locale.LC_ALL, 'en_US')

    # Numeric value representing money
    amount = 10575.50

    # Format the amount as currency using locale settings
    formatted_amount = locale.currency(amount, grouping=True)

    print(formatted_amount)