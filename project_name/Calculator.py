from .helpers import sum


class Calculator:
    """🧮 A calculator class"""

    color: str = 'blue'
    """The color of the calculator"""

    def __init__(self, color: str = 'blue') -> None:
        """Initializes the calculator

        Args:
            color (str, optional): The color of the calculator. Defaults to 'blue'.

        Returns:
            None
        """
        self.color = color

    def add_one(self, number) -> int:
        """Adds one to a number

        Args:
            number (int): The number to add one to

        Returns:
            int: The number plus one
        """

        return number + 1

    def add_two(self, number) -> int:
        """Adds two to a number

        Args:
            number (int): The number to add two to

        Returns:
            int: The number plus two
        """
        return sum(number, 2)
