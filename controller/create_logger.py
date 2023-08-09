# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

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

    # create console handler which logs even info messages
    console_handler = logging.StreamHandler()

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s, %(name)s, %(lineno)d, %(funcName)s, %(levelname)s, %(threadName)s, %(message)s"
    )

    # add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
