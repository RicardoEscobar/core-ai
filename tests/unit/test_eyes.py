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
from unittest.mock import patch
import logging
from pathlib import Path

from controller.vision.eyes import Eyes
from controller.create_logger import create_logger

# Create a logger instance
log = create_logger(
    logger_name="tests.unit.test_eyes",
    logger_filename="test_eyes.log",
    log_directory="logs/tests",
    console_logging=True,
    console_log_level=logging.INFO,
)


class TestEyes(unittest.TestCase):
    """This is the unit test class for the controller.vision.eyes module."""

    def test_eyes(self):
        """Test that the eyes class can be instantiated."""

        # Create an instance of the eyes class
        eyes = Eyes()

        # Verify that the eyes class was instantiated
        self.assertIsInstance(eyes, Eyes)
        log.info("\n✅ The eyes class was instantiated.")

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
        img_folder = str((eyes.root_folder / "img").as_posix())
        self.assertEqual(eyes.picture_output_folder, img_folder)

        self.assertTrue(hasattr(eyes, "camera_config"))
        self.assertEqual(
            eyes.camera_config,
            {
                "camera_res_height": 720,
                "camera_res_width": 1280,
                "screenshot_res_height": 720,
                "screenshot_res_width": 1280,
                "picture_output_folder": img_folder,
            },
        )

        self.assertTrue(hasattr(eyes, "detail"))
        self.assertEqual(eyes.detail, "low")

        log.info("✅ The eyes class has the correct attributes.")

    def test_get_camera_config_file(self):
        """Test that the get_camera_config_file method works as expected."""

        # Create an instance of the eyes class
        eyes = Eyes()

        # Create a variable to store the expected img folder path, as_posix() is
        # used to convert the path to a string compatible with the os and json
        # modules. The call to the as_posix() method is necessary because the
        # load_camera_config method uses the json module to load the config.json
        # file, and the json module does not accept pathlib.Path objects.
        picture_output_folder = str((eyes.root_folder / "img").as_posix())
        log.debug("picture_output_folder: %s", picture_output_folder)

        expected_camera_config = {
            "camera_res_height": 720,
            "camera_res_width": 1280,
            "screenshot_res_height": 720,
            "screenshot_res_width": 1280,
            "picture_output_folder": picture_output_folder,
        }
        log.debug("expected_camera_config: %s", expected_camera_config)

        # Verify that the load_camera_config method works as expected
        camera_config = eyes.get_camera_config_file()
        log.debug("camera_config: %s", repr(camera_config))
        self.assertIsInstance(camera_config, dict)
        self.assertEqual(camera_config, expected_camera_config)

        # Verify that the load_camera_config method works as expected when the config_json_file argument is passed
        json_file = eyes.root_folder / "config.json"
        json_file.unlink(missing_ok=True)
        camera_config = eyes.get_camera_config_file(
            config_json_file=str(eyes.root_folder / "config.json")
        )
        log.debug("camera_config: %s", camera_config)
        self.assertIsInstance(camera_config, dict)
        self.assertEqual(camera_config, expected_camera_config)

        # Remove the config.json file
        json_file.unlink(missing_ok=True)

        # Assert that if the config_json_file argument is not a string, the load_camera_config method raises a TypeError
        with self.assertRaises(TypeError):
            eyes.get_camera_config_file(
                config_json_file=eyes.root_folder / "config.json"
            )

        log.info("✅ The load_camera_config method works as expected.")

    def test_take_picture(self):
        """Test that the take_picture method works as expected."""

        # Create an instance of the eyes class
        eyes = Eyes()

        # Verify that the take_picture method works as expected
        with patch("controller.vision.eyes.log.info") as mock_info:
            # Call the function that should log "Picture taken."
            # For example:
            eyes.take_picture()

            # Check that log.info was called with the correct argument
            mock_info.assert_called_once_with("Picture taken.")

        eyes.take_picture()
        log.info("✅ The take_picture method works as expected.")


if __name__ == "__main__":
    unittest.main()
