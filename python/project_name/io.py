import logging
import os


class FileHandler:
    """📁 A class for handling input and output"""

    input = None
    output = None

    def __init__(self, input: str, output: str) -> None:
        """Initializes the FileHandler class

        Args:
            input (str): The path to the file(s) to read
            output (str): The path to the directory to write

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f"Initializing FileHandler with input path {repr(input)} and output path {repr(output)}"
        )

        self.input = input
        self.output = os.path.join(output, os.path.basename(input))

    def read_file(self) -> str:
        """Reads the file

        Returns:
            str: The contents of the file
        """

        self.logger.info(f"Reading file {repr(self.input)}")

        with open(self.input, "r") as file:
            return file.read()

    def write_file(self, contents: str) -> None:
        """Writes to the file

        Args:
            contents (str): The contents to write to the file

        Returns:
            None
        """

        self.logger.info(f"Writing {repr(contents)} to file {repr(self.output)}")

        with open(self.output, "w") as file:
            file.write(contents)

    def append_file(self, contents: str) -> None:
        """Appends to the file

        Args:
            contents (str): The contents to append to the file

        Returns:
            None
        """

        self.logger.info(f"Appending {repr(contents)} to file {repr(self.output)}")
        with open(self.output, "a") as file:
            file.write(contents)
