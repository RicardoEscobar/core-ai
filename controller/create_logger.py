import datetime
import logging
import os
from pathlib import Path


def create_logger(
    logger_name: str,
    logger_filename: str = "log.log",
    log_directory: str = "logs",
    add_date_to_filename: bool = False,
) -> logging.Logger:
    """Create a logger with a file handler that logs to a file in the specified directory.

    Args:
        logger_name (str): The name of the logger.
        logger_filename (str, optional): The name of the log file. Defaults to "log.log".
        log_directory (str, optional): The directory where the log file will be saved. Defaults to "logs".
        add_date_to_filename (bool, optional): Whether to add the date to the log file name. Defaults to False.

    Returns:
        logging.Logger: The created logger instance.
    """
    csv_compliant_file_header = "Timestamp,Logger,Line,Function,Level,Thread,Message\n"
    # Create logger directory
    logger_directory = Path(log_directory)
    if not os.path.exists(logger_directory):
        os.makedirs(logger_directory)

    # Create logger file if it doesn't exist.
    if add_date_to_filename:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = Path(logger_directory, "_".join((date, logger_filename)))
    else:
        filename = Path(logger_directory, logger_filename)

    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(csv_compliant_file_header)

    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    file_handler = logging.FileHandler(filename, encoding="utf-8", mode="a+")
    file_handler.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s, %(lineno)d, %(funcName)s, %(levelname)s, %(thread)s, %(message)s"
    )

    file_handler.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(file_handler)

    return logger