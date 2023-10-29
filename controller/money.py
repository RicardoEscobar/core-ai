"""This is a utility module to make operations with money, currencies and
convert them between cents and whole numbers. This is meant to be used to store
money values in a postgresql database as integers."""

from decimal import Decimal
from typing import Union
import locale


class Money:
    """A class to represent money values and convert them between cents and whole numbers."""

    def __init__(
        self, initial_amount: Union[int, float, Decimal] = 0, currency: str = "USD"
    ) -> None:
        """Args:
        initial_amount (Union[int, float, Decimal], optional): The amount of money. Defaults to 0.
        currency (str, optional): The currency. Defaults to "USD".
        """
        self.amount = initial_amount
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
        result = Decimal(f"{dollars}.{cents_remaining:02}")
        return result

    @staticmethod
    def currency_unit_to_cents(amount_dec: Union[int, float, Decimal]) -> int:
        """
        Convert a Decimal amount to an integer representing cents.

        Args:
            amount (Decimal): The Decimal amount to convert.

        Returns:
            int: The equivalent integer value in cents.
        """
        if not isinstance(amount_dec, (int, float, Decimal)):
            raise TypeError("The amount must be a int, float or Decimal instance.")
        cents = int(amount_dec * 100)
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
        self.amount = 0

    def __str__(self) -> str:
        """Return the amount as a string."""
        return f"${self.amount:,.2f} {self.currency}"

    def __repr__(self) -> str:
        """Return the amount as a string."""
        return f"Money({self.amount}, '{self.currency}')"


if __name__ == "__main__":
    # Example usage
    money = Money()
    money.cents = 123_45  # 12345
    print(money)
    print(money.cents)

    # Get the current locale settings
    current_locale = locale.getlocale()

    # Set the desired locale (e.g., en_US for US English)
    locale.setlocale(locale.LC_ALL, current_locale)

    # Numeric value representing money
    MAIN_AMOUNT = 10575.50

    # Format the amount as currency using locale settings
    formatted_amount = locale.currency(MAIN_AMOUNT, grouping=True)

    print(current_locale)
    print(formatted_amount)
