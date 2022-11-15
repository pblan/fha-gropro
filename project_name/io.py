import logging


class FileHandler:
    """📁 A class for handling input and output"""

    input_path = None
    output_path = None

    def __init__(self, input_path: str, output_path: str) -> None:
        """Initializes the FileHandler class

        Args:
            input_path (str): The path to the file to read
            output_path (str): The path to the file to write

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.info(
            f'Initializing FileHandler with file path {repr(input_path)}')

        self.input_path = input_path
        self.output_path = output_path

    def read_file(self) -> str:
        """Reads the file

        Returns:
            str: The contents of the file
        """

        self.logger.info(f'Reading file {repr(self.input_path)}')

        with open(self.input_path, 'r') as file:
            return file.read()

    def write_file(self, contents: str) -> None:
        """Writes to the file

        Args:
            contents (str): The contents to write to the file

        Returns:
            None
        """

        self.logger.info(
            f'Writing {repr(contents[:15] + "...") if len(contents) > 15 else repr(contents)} to file {repr(self.output_path)}')

        with open(self.output_path, 'w') as file:
            file.write(contents)

    def append_file(self, contents: str) -> None:
        """Appends to the file

        Args:
            contents (str): The contents to append to the file

        Returns:
            None
        """

        self.logger.info(
            f'Appending {repr(contents[:15] + "...") if len(contents) > 15 else repr(contents)} to file {repr(self.output_path)}')
        with open(self.output_path, 'a') as file:
            file.write(contents)
