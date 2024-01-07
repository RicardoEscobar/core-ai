from datetime import datetime
from pathlib import Path
from typing import Union

from controller.clean_filename import clean_filename


def get_audio_filepath(
        text: str,
        filename_length: int = 100,
        file_extension: str = "mp3",
        prefix: str = "",
        sufix: str = "",
        output_dir: Union[str, Path] = "./audio",
    ) -> str:
        """Return a filename for the mp3 file.
        args:
            text (str): The text to use to generate the filename.
            filename_len (int, optional): The maximum length of the filename. Defaults to 100.
            file_extension (str, optional): The file extension. Defaults to "mp3".
            prefix (str, optional): A prefix to add to the filename. Defaults to "".
            sufix (str, optional): A sufix to add to the filename. Defaults to "".
            output_dir (str, optional): The output directory. Defaults to ".".
        returns:
            str: The filename.
        """

        if isinstance(output_dir, str):
            output_dir_path = Path(output_dir)
        elif isinstance(output_dir, Path):
            output_dir_path = output_dir

        # Create the folder if it does not exist
        output_dir_path.mkdir(parents=True, exist_ok=True)

        # Clean the filename
        filename = clean_filename(text, filename_length)

        # Remake prefix and suffix
        if prefix != "":
            prefix = clean_filename("_" + prefix, filename_length)
        if sufix != "":
            sufix = clean_filename("_" + sufix, filename_length)

        # Add timestamp to filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}{prefix}_{filename}{sufix}.{file_extension}"

        # Create the file path
        result = str(output_dir_path / filename)

        return result