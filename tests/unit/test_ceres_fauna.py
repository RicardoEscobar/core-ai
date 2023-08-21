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

from controller.vtuberai.ceres_fauna import CeresFauna
from controller.vtuber_chat import TextColor
from controller.create_logger import create_logger


# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_ceres_fauna",
    logger_filename="test_ceres_fauna.log",
    log_directory="logs/tests",
    console_logging=True,
    console_log_level=logging.INFO,
)

class TestCeresFauna(unittest.TestCase):
    def test_init(self):
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        self.assertEqual(vtuber.name, "Ceres Fauna")
        self.assertEqual(vtuber.age, 18)
        self.assertEqual(vtuber.gpt_model, "gpt-4")

    def test_str(self):
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        self.assertEqual(str(vtuber), "Ceres Fauna is a 18 year old VTuberAI")

    def test_repr(self):
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        self.assertEqual(
            repr(vtuber),
            "CearesFauna(name=Ceres Fauna, age=18, gpt_model=gpt-4)"
        )

    def test_chat(self):
        """Test the Twitch chat method of the VTuberAI"""

        # Assert that the 'Twitch' object is not None when creating a 'CeresFauna' object
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        self.assertIsNotNone(vtuber.twitch)

if __name__ == "__main__":
    unittest.main()