"""This is the unit test class for the controller.vision.eyes module."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    if str(project_directory) not in sys.path:
        sys.path.append(str(project_directory))

import unittest
import logging

from controller.vision.eyes import Eyes
from controller.create_logger import create_logger

# Create a logger instance
log = create_logger(
    logger_name="tests.unit.test_eyes",
    logger_filename="test_eyes.log",
    log_directory="logs/tests",
    console_logging=False,
    console_log_level=logging.INFO,
)


class TestEyes(unittest.TestCase):
    """This is the unit test class for the controller.vision.eyes module."""

    def test_eyes(self):
        """Test that the eyes class can be instantiated."""

        log.info("===Testing eyes class===")
        # Create an instance of the eyes class
        eyes = Eyes()

        # Verify that the eyes class was instantiated
        self.assertIsInstance(eyes, Eyes)
        log.debug("✅ The eyes class was instantiated.")

        # Verify that the eyes class has the correct attributes
        self.assertTrue(hasattr(eyes, "username"))
        self.assertEqual(eyes.username, "Jorge")

        self.assertTrue(hasattr(eyes, "config_json_path"))
        self.assertEqual(
            eyes.config_json_path,
            Path(r"C:/Users/Jorge/AppData/LocalLow/VRChat/VRChat/config.json"),
        )

        self.assertTrue(hasattr(eyes, "root_folder"))
        self.assertEqual(eyes.root_folder, Path(__file__).parent.parent.parent)

        self.assertTrue(hasattr(eyes, "picture_output_folder"))
        img_folder = str(eyes.root_folder / "img")
        self.assertEqual(eyes.picture_output_folder, img_folder)

        self.assertTrue(hasattr(eyes, "camera_config"))
        self.assertEqual(
            eyes.camera_config,
            {
                "camera_res_height": 720,
                "camera_res_width": 1280,
                "screenshot_res_height": 720,
                "screenshot_res_width": 1280,
                "picture_output_folder": str(eyes.root_folder / "img"),
            },
        )

        self.assertTrue(hasattr(eyes, "detail"))
        self.assertEqual(eyes.detail, "low")

        log.debug("✅ The eyes class has the correct attributes.")

    def test_load_camera_config(self):
        """Test that the load_camera_config method works as expected."""

        log.info("===Testing load_camera_config method===")
        # Create an instance of the eyes class
        eyes = Eyes()

        # Create a variable to store the expected img folder path, as_posix() is
        # used to convert the path to a string compatible with the os and json
        # modules
        img_folder = str((eyes.root_folder / "img").as_posix())

        expected_camera_config = {
            "camera_res_height": 720,
            "camera_res_width": 1280,
            "screenshot_res_height": 720,
            "screenshot_res_width": 1280,
            "picture_output_folder": img_folder,
        }
        log.debug("expected_camera_config: %s", repr(expected_camera_config))

        # Verify that the load_camera_config method works as expected
        camera_config = eyes.load_camera_config()
        self.assertIsInstance(camera_config, dict)
        log.debug("camera_config: %s", repr(camera_config))
        self.assertEqual(camera_config, expected_camera_config)

        log.debug("✅ The load_camera_config method works as expected.")


if __name__ == "__main__":
    unittest.main()
