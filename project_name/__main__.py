import configparser
import logging
from project_name import FileHandler, Parser, find_location
import os
import argparse


def setup():
    """Sets up the logger and config"""

    # reading the config file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # setting up the logger
    logging_dir = find_location(config["io"]["logging_dir"])

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y/%m/%d %I:%M:%S %p",
        handlers=[
            logging.FileHandler(
                filename=os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "logs",
                    "project_name.log",
                ),
                mode="w",
            ),
        ],
    )

    logging.info("Logging initialized")
    print(f"Logging to {os.path.join(logging_dir, 'project_name.log')}")

    # Logging configuration
    for section in config.sections():
        for key, value in config[section].items():
            logging.debug(f"[CONFIG] {section}.{key} = {value}")

    logging.debug("Config file read")

    # Setup: Setting up Arguments
    logging.info("Reading arguments")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-f", help="File or directory to parse")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--debug", "-d", help="Debug mode", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.getLogger().setLevel(logging.DEBUG)

        logging.info("Debug mode enabled")

    logging.debug("Arguments read")

    # logging configuration
    for key, value in vars(args).items():
        logging.debug(f"[ARGUMENT] {key} = {value}")

    # use defaults if no arguments are passed
    if args.input is None:
        args.input = find_location(config["io"]["input_dir"])

    logging.debug(f"Input file/directory: {args.input}")

    if args.output is None:
        args.output = find_location(config["io"]["output_dir"])

    logging.debug(f"Output directory: {args.output}")

    # check if files/directories exist
    if not os.path.exists(args.input):
        logging.error(f"Input file/directory {args.input} does not exist")
        exit(1)

    if not os.path.exists(args.output):
        logging.error(
            f"Output directory {args.output} does not exist or is not a directory"
        )
        exit(1)

    logging.info("Setup complete")
    return config, args


config, args = setup()

logging.info("Starting project_name")

input_queue = [args.input] if os.path.isfile(args.input) else os.listdir(args.input)

for file in input_queue:
    # skip .gitkeep
    if file == ".gitkeep":
        continue

    file_handler = FileHandler(os.path.join(args.input, file), args.output)
    contents = file_handler.read_file()

    parser = Parser(contents)
    result = parser.parse()

    file_handler.write_file(result)

# Ending the program
logging.info("Ending project_name")
