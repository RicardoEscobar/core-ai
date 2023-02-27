import datetime
import logging
import os
from pathlib import Path


def create_logger(logger_name: str, logger_filename: str, log_directory: str = 'logs') -> logging.Logger:
    """Create a logger with a file handler that logs to a file in the specified directory.

    Args:
        name (str): The name of the logger.
        log_directory (str, optional): The directory in which to create the log file. Defaults to 'logs'.
        log_filename (str, optional): The name of the log file. If None, a file with the current date will be created. Defaults to None.

    Returns:
        logging.Logger: The created logger instance.
    """
    # Create logger directory
    logger_directory = Path(log_directory)
    if not os.path.exists(logger_directory):
        os.makedirs(logger_directory)

    # Create logger file if it doesn't exist.
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = Path(logger_directory, '_'.join((date, logger_filename)))

    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(
                'Timestamp | Logger | Function | Line | Level | Message\n')

    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    file_handler = logging.FileHandler(
        filename, encoding='utf-8', mode='a+')
    file_handler.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(funcName)s | %(lineno)d | %(levelname)s | %(message)s')

    file_handler.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(file_handler)

    logger.info('Logger for %s module created.', logger_name)
    return logger
