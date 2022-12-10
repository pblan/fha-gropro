import argparse
import configparser
import logging
import os
import sys

import spidercam_simulator


def setup():
    """Sets up the logger and config"""

    # reading the config file
    cfg = configparser.ConfigParser()
    # parent of os.path.dirname(__file__)
    cfg_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
    print(f"Config file: {cfg_file}")
    cfg.read(cfg_file)

    # setting up the logger
    logging_dir = spidercam_simulator.find_location(cfg["io"]["logging_dir"])

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
        datefmt="%Y/%m/%d %I:%M:%S %p",
        handlers=[
            logging.FileHandler(
                filename=os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "logs",
                    "spidercam_simulator.log",
                ),
                mode="w",
            ),
        ],
    )

    logging.info("Logging initialized")
    print(f"Logging to {os.path.join(logging_dir, 'spidercam_simulator.log')}")

    # Logging configuration
    for section in cfg.sections():
        for key, value in cfg[section].items():
            logging.debug("Config: %s.%s = %s", section, key, value)

    logging.debug("Config file read")

    # Setup: Setting up Arguments
    logging.info("Reading arguments")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="File or directory to parse")
    parser.add_argument(
        "--output", "-o", help="Output directory (needs to be different from input)"
    )
    parser.add_argument("--debug", "-d", help="Debug mode", action="store_true")
    parser.add_argument(
        "--no-plot", "-np", help="Disable plotting", action="store_true"
    )
    ags = parser.parse_args()

    if ags.debug:
        # logging.getLogger().addHandler(logging.StreamHandler())
        logging.getLogger().setLevel(logging.DEBUG)

        logging.info("Debug mode enabled")

    logging.debug("Arguments read")

    # logging configuration
    for key, value in vars(ags).items():
        logging.debug("Argument: %s = %s", key, value)

    # use defaults if no arguments are passed
    if ags.input is None:
        ags.input = cfg["io"]["input_dir"]

    ags.input = spidercam_simulator.find_location(ags.input)

    logging.debug("Input file/directory: %s", ags.input)

    if ags.output is None:
        ags.output = cfg["io"]["output_dir"]

    ags.output = spidercam_simulator.find_location(ags.output)

    logging.debug("Output directory: %s", ags.output)

    # check if files/directories exist
    if not os.path.exists(ags.input):
        logging.error("Input file/directory %s does not exist", ags.input)
        sys.exit(1)

    if not os.path.exists(ags.output):
        logging.error(
            "Output directory %s does not exist. Please create it first.", ags.output
        )
        sys.exit(1)

    # check if input and output are the same
    if os.path.samefile(ags.input, ags.output):
        logging.error("Input and output directories are the same")
        sys.exit(1)

    logging.info("Setup complete")
    return cfg, ags


config, args = setup()

logging.info("Starting spidercam_simulator")

input_queue = [args.input] if os.path.isfile(args.input) else os.listdir(args.input)

logging.info("Found %s files/directories to process", len(input_queue))

for file in input_queue:
    if file == ".gitkeep":
        continue

    logging.info("Processing %s", file)

    file_handler = spidercam_simulator.FileHandler(
        os.path.join(args.input, file), args.output
    )
    contents = file_handler.read_file()

    logging.debug("File contents: %s", contents)

    # parse the file but skip if error
    try:
        input_dict = spidercam_simulator.Parser.parse_input(contents)
    except ValueError as exc:
        logging.error("Error parsing file: %s", exc)
        print(f"Error parsing file {file}: {exc}")
        continue

    logging.debug("Input dictionary: %s", input_dict)

    controller = spidercam_simulator.Controller.from_dict(input_dict)

    logging.info("Running controller %s", repr(controller))

    cam_positions, rope_lengths = controller.run()

    logging.debug("Cam positions: %s", cam_positions)
    logging.debug("Rope lengths: %s", rope_lengths)

    output1, output2 = spidercam_simulator.Parser.parse_output(
        input_dict["dim"], input_dict["freq"], cam_positions, rope_lengths
    )

    file_handler.write_files(output1, output2)

    if not args.no_plot:
        plotter = spidercam_simulator.Plotter(
            input_dict["dim"],
            input_dict["freq"],
            cam_positions,
            rope_lengths,
            args.output,
            os.path.splitext(file)[0],
        )

        plotter.plot()

    # cleanup
    del file_handler
    del contents
    del input_dict
    del controller
    del cam_positions
    del rope_lengths
    del output1
    del output2

    logging.info("Finished processing %s", file)

    # file_handler.write_file(parsed)

# Ending the program
logging.info("Ending spidercam_simulator")
