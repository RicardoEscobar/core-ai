"""This module is used to remove the code blocks from markdown files and return the filtered text to be used on a text to speak software."""
from pathlib import Path
import logging


class CodeFilter:
    """This class is used to remove the code blocks from markdown files and return the filtered text to be used on a text to speak software."""

    def __init__(self, text: str = '', file_path: str = ''):
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

        # If file_path is not None, read the file and store the text in self.text_from_file
        self.text_from_file = ''
        if self.file_path is not None:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.text_from_file = file.read()

    @property
    def filtered_str(self) -> str:
        """This method is used to remove the code blocks from str variables and return the filtered text to be used on a text to speak software.

        Returns
        -------
        str
            The filtered text.
        """

        filtered_str = ''
        code_block = False

        for line in self.text.splitlines():
            self.logger.debug("Line: %s", repr(line))
            if line.startswith("```"):
                self.logger.debug("Code block: %s", repr(line))
                code_block = not code_block
            elif not code_block:
                filtered_str += line + "\n"

        # Remove whitespace.
        filtered_str = filtered_str.strip()

        # Remove empty lines.
        filtered_str = "\n".join([line for line in filtered_str.splitlines() if line.strip() != ""])

        self.logger.debug("Filtered text: %s", repr(filtered_str))

        return filtered_str

    @filtered_str.setter
    def filtered_str(self, value: str):
        """This method is used to set the filtered_str property."""
        self.logger.info("Setting filtered_str property with value: %s", repr(value))
        self.filtered_str = value

    @filtered_str.deleter
    def filtered_str(self):
        """This method is used to delete the filtered_str property."""
        self.logger.info("Deleting filtered_str property.")
        del self.filtered_str

    @property
    def filtered_file_str(self) -> str:
        """This method is used to remove the code blocks from markdown files and return the filtered text to be used on a text to speak software."""
        # Validate that self.file_path is not None
        if self.file_path is None:
            raise ValueError("self.file_path is None, There is no file to read.")
        else:
            self.logger.debug("self.file_path: %s", repr(self.file_path))

        # Open the file and read the contents
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.text = file.read()
        
        # Calls the filtered_str property and returns the filtered text.
        return self.filtered_str
    
    @filtered_file_str.setter
    def filtered_file_str(self, value: str):
        """This method is used to set the filtered_file_str property."""
        self.logger.info("Setting filtered_file_str property with value: %s", repr(value))
        self.filtered_file_str = value

    @filtered_file_str.deleter
    def filtered_file_str(self):
        """This method is used to delete the filtered_file_str property."""
        self.logger.info("Deleting filtered_file_str property.")
        del self.filtered_file_str

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
