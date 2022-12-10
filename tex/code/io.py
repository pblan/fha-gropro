import logging
import os

import numpy as np


class FileHandler:
    """ A class for handling input and output"""

    def __init__(self, input_file: str, output_dir: str) -> None:
        """Initializes the FileHandler class

        Args:
            input_file (str): The path to the file to read
            output_dir (str): The path to the directory to write

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            "Initializing FileHandler with input_file %s and output_dir %s",
            input_file,
            output_dir,
        )

        self.input_file = input_file
        self.output_dir = output_dir
        # removes file ending from input
        self.output_files = (
            os.path.join(
                output_dir, os.path.basename(input_file).split(".")[0] + "_1.csv"
            ),
            os.path.join(
                output_dir, os.path.basename(input_file).split(".")[0] + "_2.csv"
            ),
        )

    def read_file(self) -> str:
        """Reads the file

        Returns:
            str: The contents of the file
        """

        self.logger.info("Reading file %s", self.input_file)

        with open(self.input_file, "r", encoding="utf-8") as file:
            return file.read()

    def write_files(self, output1: str, output2: str) -> None:
        """Writes the output to two files

        Args:
            output1 (str): The contents to write to the first file
            output2 (str): The contents to write to the second file

        Returns:
            None
        """

        self.logger.info(
            "Writing output to files %s and %s",
            self.output_files[0],
            self.output_files[1],
        )

        with open(self.output_files[0], "w", encoding="utf-8") as file:
            file.write(output1)

        with open(self.output_files[1], "w", encoding="utf-8") as file:
            file.write(output2)


def find_location(file: str) -> str:
    """ Finds the location of the given file/directory
    Looks in the following locations:
        - The current working directory
        - The directory of the script
        - The directory of the script's parent
        - The home directory
        - The root directory

    Args:
        file (str): The path to the given file/directory

    Returns:
        str: The absolute path to the given file/directory
    """

    try:
        logger = logging.getLogger(__name__)
        logger.debug("Finding location of file/directory %s", file)
    except NameError:
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
        logger.debug("Checking location %s", location)
        if os.path.exists(os.path.join(location, file)):
            # log absolute path
            logger.debug("Found file/directory at %s", os.path.join(location, file))
            return os.path.join(location, file)

    raise FileNotFoundError(f"Could not find file/directory {repr(file)}")


class Parser:
    """ A class for parsing input strings"""

    logger = logging.getLogger(__name__)

    @staticmethod
    def parse_input(string: str) -> dict:
        """Parses the given string

        Example file contents:
        ```
        # Beispiel 2
        dim 70 100 30
        start 10 80 10
        vmax 6
        amax 2
        freq 2
        0 50 40 30      # 1:
        20 10 80 10     # 2: Anweisung beginnt nach Ende der vorherigen
        22 50 40 30     # 3: Die Bremsung der vorherigen Anweisung wird eingeleitet
        23 35 50 30     # 4: Bremsung von Anweisung 2 noch nicht beendet -> Anweisung 3 wird ignoriert
        27.5 10 80 20   # 5: Anweisung 5 endete nicht zu den diskreten Zeitpunken -> offset beachten
        ```

        Args:
            string (str): The string to parse

        Returns:
            dict: The parsed string
                - dim (tuple): The dimensions of the field
                - start (tuple): The starting position of the spidercam
                - max_velocity (float): The maximum velocity of the spidercam
                - acceleration (float): The maximum acceleration of the spidercam
                - freq (float): The discrete time frequency
                - instructions (list): The instructions for the spidercam
        """

        Parser.logger.debug("Parsing string %s", string)

        lines = string.splitlines()
        instructions = []

        # Clean up the lines and remove comments
        for i, line in enumerate(lines):
            lines[i] = line.split("#")[0].strip()

        # Remove empty lines
        lines = list(filter(None, lines))

        # Parse the lines
        for i, line in enumerate(lines):
            if line.startswith("dim"):
                dim = tuple(map(int, line.split()[1:]))
            elif line.startswith("start"):
                start = tuple(map(int, line.split()[1:]))
            elif line.startswith("vmax"):
                max_velocity = float(line.split()[1])
            elif line.startswith("amax"):
                acceleration = float(line.split()[1])
            elif line.startswith("freq"):
                freq = float(line.split()[1])
            else:
                instructions.append(Instruction.parse(line))

        # Check if the dimensions are valid
        if len(dim) != 3 or any(d <= 0 for d in dim):
            raise ValueError("The dimensions are invalid")

        # Check if the starting position is valid
        if len(start) != 3 or not all(0 <= i <= j for i, j in zip(start, dim)):
            raise ValueError("The starting position is invalid")

        # Check if the maximum velocity is valid
        if max_velocity <= 0:
            raise ValueError("The maximum velocity is invalid")

        # Check if the maximum acceleration is valid
        if acceleration <= 0:
            raise ValueError("The maximum acceleration is invalid")

        # Check if the discrete time frequency is valid
        if freq <= 0:
            raise ValueError("The discrete time frequency is invalid")

        # Check if the instructions are valid
        if len(instructions) == 0:
            raise ValueError("No instructions found")

        for i, instruction in enumerate(instructions):
            if not all(0 <= j <= k for j, k in zip(instruction.destination, dim)):
                raise ValueError(f"Instruction {i + 1} is invalid")

        return {
            "dim": dim,
            "start": start,
            "max_velocity": max_velocity,
            "acceleration": acceleration,
            "freq": freq,
            "instructions": instructions,
        }

    # returns two strings
    @staticmethod
    def parse_output(
        dim: tuple,
        freq: float,
        cam_positions: list[tuple],
        rope_lengths: list[tuple],
    ) -> tuple:
        """Parses the output

        Example file contents (first output: lengths of the ropes):
        ```
        83.06623, 82.9059, [...], 64.0056, 64.0312 # Rope 1
        101.9803, 101.9803, [...], 101.9803, 101.9803 # Rope 2
        101.9803, 101.9803, [...], 101.9803, 101.9803 # Rope 3
        101.9803, 101.9803, [...], 101.9803, 101.9803 # Rope 4
        ```

        Example file contents (second output: dimensions, time stamps, positions of the camera):
        ```
        70, 100, 30 # Dimensions
        0.0, 0.5, 1.0, [...], 20.5, 21.0 # Time stamps
        10.0, 10.16, 10.66, [...], 20.0, 20.0 # x coordinates
        80.0, 80.0, 80.0, [...], 80.0, 80.0 # y coordinates
        10.0, 10.0, 10.0, [...], 10.0, 10.0 # z coordinates
        ```


        Args:
            dim (tuple): The dimensions of the field
            freq (float): The discrete time frequency
            cam_positions (list[tuple]): The positions of the camera
            rope_lengths (list[tuple]): The lengths of the ropes

        Returns:
            str: The parsed output
        """

        Parser.logger.info(
            "Parsing output with #cam_positions=%d and #rope_lengths=%d",
            len(cam_positions),
            len(rope_lengths),
        )

        # Using numpy to transform the lists into numpy arrays for easier handling
        cam_positions = np.array(cam_positions)
        rope_lengths = np.array(rope_lengths)

        # transposing the arrays to get the correct shape
        cam_positions = cam_positions.T
        rope_lengths = rope_lengths.T

        # creating the time stamps
        time_stamps = np.arange(0, len(cam_positions[0]) / freq, 1 / freq)

        # creating the output strings
        output1 = "\n".join(",".join(map(str, rope)) for rope in rope_lengths)

        # adding the dimensions to the output
        output2 = f"{dim[0]},{dim[1]},{dim[2]}\n"

        # adding the time stamps to the output
        output2 += ",".join(map(str, time_stamps)) + "\n"

        # adding the positions of the camera to the output
        output2 += ",".join(map(str, cam_positions[0])) + "\n"
        output2 += ",".join(map(str, cam_positions[1])) + "\n"
        output2 += ",".join(map(str, cam_positions[2])) + "\n"

        # output2 = "\n".join(
        #     ",".join(map(str, line)) for line in [dim, time_stamps, *cam_positions]
        # )

        Parser.logger.debug("Parsed output")

        return output1, output2


class Instruction:
    """ A class for defining an instruction"""

    def __init__(self, start_time: float = 0.0, destination: tuple = (0, 0, 0)) -> None:
        """Initializes the Instruction class

        Args:
            start_time (float, optional): The time to start the instruction. Defaults to 0.0.
            destination (tuple, optional): The destination of the instruction. Defaults to (0, 0, 0).

        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            "Initializing Instruction with start_time=%f and destination=%s",
            start_time,
            destination,
        )
        self.start_time = start_time
        self.destination = destination

    @classmethod
    def parse(cls, data: str) -> "Instruction":
        """Parses an instruction from a string

        Args:
            data (str): The string to parse the instruction from
                - format: start_time x y z

        Returns:
            Instruction: The instruction
        """
        cls.logger = logging.getLogger(__name__)
        cls.logger.debug("Parsing instruction from %s", data)

        try:
            start_time, x, y, z = data.split(" ")
        except ValueError as exp:
            raise ValueError(
                f"Invalid instruction format (expected: start_time x y z), got: {data}"
            ) from exp

        return cls(float(start_time), (float(x), float(y), float(z)))

    def __repr__(self) -> str:
        """Returns the representation of the instruction

        Args:
            None

        Returns:
            str: The representation of the instruction
        """
        return (
            f"Instruction(start_time={self.start_time}, destination={self.destination})"
        )
