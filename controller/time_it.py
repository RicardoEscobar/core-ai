"""This module contains a time_it decorator for timing function calls."""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent
    sys.path.append(str(root_folder))

import time
from functools import wraps
import logging

from controller.create_logger import create_logger

# Create a logger for this module
module_logger = create_logger(
    logger_name="controller.time_it",
    logger_filename="time_it.log",
    log_directory="logs",
    add_date_to_filename=False,
    console_logging=True,
    console_log_level=logging.INFO,
)


def time_it(func):
    """Decorator to time function calls."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function for time_it decorator."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        module_logger.info(
            "Function %s took %s seconds to complete",
            func.__name__,
            round(end_time - start_time, 2),
        )
        return result

    return wrapper


if __name__ == "__main__":
    @time_it
    def test_function():
        """Test function for time_it decorator."""
        time.sleep(1)


    test_function()
