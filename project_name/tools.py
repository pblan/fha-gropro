import logging


class Parser:
    """📝 A class for parsing strings"""

    def __init__(self, string: str) -> None:
        """Initializes the Parser class

        Args:
            string (str): The string to parse

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.info(f'Initializing Parser with string {repr(string[:15] + "...") if len(string) > 15 else repr(string)}')
        self.string = string

    def parse(self) -> str:
        """Parses the given string

        Example file contents:
        ```
        # example input file
        """

        self.logger.info(f'Parsing string {repr(self.string[:15] + "...") if len(self.string) > 15 else repr(self.string)}')

        return self.string + '\n# but now it\'s parsed!'


class Calculator:
    """🧮 A calculator class"""

    color: str = 'blue'

    def __init__(self, color: str = 'blue') -> None:
        """Initializes the calculator

        Args:
            color (str, optional): The color of the calculator. Defaults to 'blue'.

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.info(f'Initializing calculator with color {color}')

        self.color = color

    def sum(a, b):
        """Adds two numbers together

        Args:
            a (int): The first number
            b (int): The second number

        Returns:
            int: The sum of the two numbers
        """

        return a + b

    def add_one(self, number) -> int:
        """Adds one to a number

        Args:
            number (int): The number to add one to

        Returns:
            int: The number plus one
        """

        logging.info(f'Adding one to {number}')

        return number + 1

    def add_two(self, number) -> int:
        """Adds two to a number

        Args:
            number (int): The number to add two to

        Returns:
            int: The number plus two
        """

        logging.info(f'Adding two to {number}')

        return sum(number, 2)
