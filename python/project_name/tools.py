import logging
import time
import os


def find_location(input: str) -> str:
    """🔍 Finds the location of the input file/directory
    Looks in the following locations:
        - The current working directory
        - The directory of the script
        - The directory of the script's parent
        - The home directory
        - The root directory

    Args:
        input (str): The path to the input file/directory

    Returns:
        str: The path to the input file/directory
    """

    try:
        logger = logging.getLogger(__name__)
        logger.info(f"Finding location of file/directory {repr(input)}")
    except:
        pass

    locations = [
        os.getcwd(),  # Current working directory
        os.path.dirname(os.path.realpath(__file__)),  # Directory of the script
        os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))
        ),  # Directory of the script's parent
        os.path.expanduser("~"),  # Home directory
        os.path.sep,  # Root directory
    ]

    for location in locations:
        if os.path.exists(os.path.join(location, input)):
            return os.path.join(location, input)

    raise FileNotFoundError(f"Could not find file/directory {repr(input)}")


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
        self.logger.info(f"Initializing Parser with string {repr(string)}")
        self.string = string

    def parse(self) -> str:
        """Parses the given string

        Example file contents:
        ```
        # example input file
        """

        self.logger.info(f"Parsing string {repr(self.string)}")

        start_time = time.time()

        total_time = time.time() - start_time
        total_time = round(total_time * 1000, 3)

        self.logger.info(f"Finished parsing string in {total_time}ms")

        return self.string + "\n# but now it's parsed!"
