"""This module is for the eyes of the AI, the vision, the ability to see."""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent.parent
    sys.path.append(str(root_folder))

from pathlib import Path
import getpass
import json
from typing import Dict, Literal
import logging
import time
import subprocess
import base64

from openai import OpenAI
import pyautogui

from controller.create_logger import create_logger
from controller.load_openai import load_openai
from controller.time_it import time_it


# Load the OpenAI API key from the .env file
load_openai()

# Create an instance of the OpenAI class
client = OpenAI()

# Run the picture_detector.py script in a subprocess to watch for new pictures
# and process them
picture_detector_process = subprocess.Popen(["python", "controller/vision/picture_detector.py"])

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
    picture_output_folder = str((root_folder / "img").as_posix())

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

    def get_camera_config_file(self, config_json_file: str = None) -> Dict:
        """Returns the camera config from the config.json file as a dictionary."""
        # Validate that the config_json_file is not None
        if config_json_file is None:
            config_json_file = self.config_json_file

        # Validate that the config_json_file is a string
        if not isinstance(config_json_file, str):
            raise TypeError(
                f"config_json_file must be a string, not {type(config_json_file)}"
            )

        try:
            with open(config_json_file, "r", encoding="utf-8") as file:
                config = json.load(file)
            log.debug("config = %s", repr(config))
        except FileNotFoundError:
            # If the config.json file is not found, use the default camera config
            with open(config_json_file, "w", encoding="utf-8") as file:
                json.dump(self.camera_config, file, indent=4)
            log.error(
                "The config.json file was not found at %s, using the default camera config. One was created at that location as: %s",
                config_json_file,
                self.config_json_path,
            )
            return self.camera_config
        else:
            return config

    @staticmethod
    def take_picture():
        """Take a picture using the in game VRChat Camera or multi layer camera.
        The picture will be saved in the picture_output_folder."""
        pyautogui.mouseDown(button="left")
        pyautogui.sleep(0.5)  # Keep the button pressed for half a second
        pyautogui.mouseUp(button="left")
        log.info("Picture taken.")

    # @time_it
    @staticmethod
    # Function to encode the image
    def encode_image(image_path: str) -> bytes:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    @time_it
    def vision_file(
        image_path: str = r"C:\Users\Jorge\git\core-ai\img\latest_picture_512x512.png",
        gpt_model: str = "gpt-4-vision-preview",
        prompt: str = "Explain this image:",
        max_tokens: int = 300,
        detail: Literal["low", "high"] = "low",
    ) -> str:
        """Returns the response from the OpenAI API after sending an image."""

        # Getting the base64 string
        base64_image = Eyes.encode_image(image_path)

        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": detail,
                            },
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )

        # Return the text from the first choice
        return response.choices[0].message.content


if __name__ == "__main__":
    time.sleep(2)
    Eyes.take_picture()
    time.sleep(2)
    # If the image_path = r"C:\Users\Jorge\git\core-ai\img\latest_picture_512x512.png" exist and is a valid png file, then run the vision_file() function
    filepath = Path(r"C:\Users\Jorge\git\core-ai\img\latest_picture_512x512.png")
    while True:
        if filepath.is_file() and filepath.__sizeof__() > 0:
            print("The file exists.")
            print(Eyes.vision_file())
            break
        else:
            print("The file does not exist.")
            time.sleep(2)
            continue

    picture_detector_process.terminate()
