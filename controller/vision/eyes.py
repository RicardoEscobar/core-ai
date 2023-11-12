"""This module is for the eyes of the AI, the vision, the ability to see."""
from pathlib import Path
import getpass
import json
from typing import Dict, Literal
import logging

from controller.create_logger import create_logger

# Create a logger instance
log = create_logger(
    logger_name="controller.vision.eyes",
    logger_filename="eyes.log",
    log_directory="logs",
    console_logging=True,
    console_log_level=logging.INFO,
)


class Eyes:
    """The eyes of the AI, the vision, the ability to see. This is achieved by
    taking a picture using the ingame VRChat Camera or multi layer camera, then
    detect the newly taken pictures and process them."""

    # Default values for the eyes class
    username = getpass.getuser()

    # This is the path to the config.json file for VRChat
    config_json_path = Path(
        r"C:/Users/" + username + r"/AppData/LocalLow/VRChat/VRChat/config.json"
    )

    # This is the path to the root folder of the project
    root_folder = Path(__file__).parent.parent.parent

    # This is the path to the folder where the pictures will be saved,
    # as_posix() is used to convert the path to a string compatible with the os
    # and json modules
    picture_output_folder = str(root_folder / "img")

    # This is the default camera config to be saved as a json file at the config_json_path
    camera_config = {
        "camera_res_height": 720,
        "camera_res_width": 1280,
        "screenshot_res_height": 720,
        "screenshot_res_width": 1280,
        "picture_output_folder": picture_output_folder,
    }

    def __init__(
        self,
        picture_output_folder: str = picture_output_folder,
        config_json_file: str = str(config_json_path),
        camera_config: Dict = None,
        detail: Literal["low", "high"] = "low",
    ):
        """Initialize the eyes of the AI, the vision, the ability to see."""
        self.picture_output_folder = picture_output_folder
        log.debug("picture_output_folder = %s", repr(picture_output_folder))
        self.config_json_file = config_json_file
        if camera_config is None:
            camera_config = self.camera_config
        self.detail = detail

    def load_camera_config(self):
        """Load the camera config from the config.json file."""
        with open(self.config_json_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        log.debug("config = %s", repr(config))
        return config
