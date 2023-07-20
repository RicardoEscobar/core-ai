"""This module is used to remove the code blocks from markdown files and return the filtered text to be used on a text to speak software."""
from pathlib import Path
import logging


class CodeFilter:
    """This class is used to remove the code blocks from markdown files and return the filtered text to be used on a text to speak software."""

    def __init__(self, text: str, file_path: str = ''):
        """The constructor for the CodeFilter class.

        Parameters
        ----------
        text : str
            The text to be filtered.
        """
        # Initialize logging from code_filter.py
        self.setup_logging()

        self.text = text
        if file_path == '':
            self.file_path = None
        else:
            self.file_path = Path(file_path)

    def filter_code_block(self):
        """This method is used to remove the code blocks from markdown files or str variables and return the filtered text to be used on a text to speak software.

        Returns
        -------
        str
            The filtered text.
        """
        filtered_text = ""
        code_block = False
        for line in self.text.splitlines():
            self.logger.debug("Line: %s", repr(line))
            if line.startswith("```"):
                self.logger.debug("Code block: %s", repr(line))
                code_block = not code_block
            elif not code_block:
                filtered_text += line + "\n"
                self.logger.debug("Filtered text: %s", repr(filtered_text))

        # Remove trailing whitespace and newlines.
        filtered_text = filtered_text.rstrip()
        self.logger.debug("Filtered text: %s", repr(filtered_text))
        
        return filtered_text

    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        cls.file_handler = logging.FileHandler("logs/code_filter.log")
        cls.file_handler.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        cls.console_handler = logging.StreamHandler()
        cls.console_handler.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formater_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        cls.formatter = logging.Formatter(formater_str)
        cls.console_handler.setFormatter(cls.formatter)
        cls.file_handler.setFormatter(cls.formatter)

        # add the handlers to the logger
        cls.logger.addHandler(cls.console_handler)
        cls.logger.addHandler(cls.file_handler)
        cls.logger.debug("Logging configuration finished.")
