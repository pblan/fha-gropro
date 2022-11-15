import configparser
import logging
from project_name import FileHandler, Parser
import time
import os

# Setting up Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
    datefmt='%Y/%m/%d %I:%M:%S %p',
    handlers=[
        # logging.StreamHandler(),
        logging.FileHandler(
            filename=f'logs/project_name.log', mode='w')
    ]
)

logging.info('Logging initialized')

# Setting up ConfigParser
logging.info('Reading config file')

config = configparser.ConfigParser()
config.read('config.ini')

logging.info('Config file read')

for section in config.sections():
    for key, value in config[section].items():
        logging.info(f'[CONFIG] {section}.{key} = {value}')


# Starting the program

logging.info('Starting project_name')

# for each file in the specified directory in config['io']['input_dir']
for input_file in os.listdir(config['io']['input_dir']):
    logging.info(f'Processing {input_file}')

    start_time = time.time()

    # read the file
    fh = FileHandler(os.path.join(config['io']['input_dir'], input_file),
                        os.path.join(config['io']['output_dir'], input_file))
    contents = fh.read_file()

    # parse the file
    parser = Parser(contents)
    parsed_contents = parser.parse()

    # write the file
    fh.write_file(parsed_contents)

    # log in milliseconds
    total_time = time.time() - start_time
    total_time = total_time * 1000

    logging.info(f'Finished processing {input_file} in {total_time.__round__(3)}ms')

