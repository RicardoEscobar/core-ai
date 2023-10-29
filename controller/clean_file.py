"""Clean a filename, by removing special characters and spaces."""
import re


def clean_filename(
        filename: str,
        filename_length: int = 100,
    ) -> str:
        """Clean a filename.
        Args:
            filename (str): The filename to clean.
            filename_length (int, optional): The maximum length of the filename. Defaults to 100."""
        filename = re.sub(r"[^\w\s-]", "", filename[:filename_length]).strip()
        filename = re.sub(r"[-\s]+", "-", filename)
        filename = re.sub(r"[.,:;¿?¡!\"]", "", filename)

        return filename