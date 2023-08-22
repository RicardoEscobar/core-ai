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
from controller.create_logger import create_logger


# Create a logger instance
module_logger = create_logger(
    logger_name="tests.unit.test_ceres_fauna",
    logger_filename="test_ceres_fauna.log",
    log_directory="logs/tests",
    console_logging=False,
    console_log_level=logging.INFO,
)


class TestCeresFauna(unittest.TestCase):
    """Test the CeresFauna class"""

    logger = module_logger

    def test_init(self):
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        self.assertEqual(vtuber.name, "Ceres Fauna")
        self.assertEqual(vtuber.age, 18)
        self.assertEqual(vtuber.gpt_model, "gpt-4")
        self.assertEqual(vtuber.language, CeresFauna.language)
        self.assertEqual(vtuber.personality, CeresFauna.personality)
        self.assertEqual(vtuber.personality_type, CeresFauna.personality_type)
        self.logger.info("Tested the __init__ method of the CeresFauna class.")

    def test_str(self):
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        self.assertEqual(str(vtuber), "Ceres Fauna is a 18 year old VTuberAI")
        self.logger.info("Tested the __str__ method of the CeresFauna class.")

    def test_repr(self):
        vtuber = CeresFauna(name="Ceres Fauna", age=18, gpt_model="gpt-4")
        expected = "CeresFauna(name={}, age={}, gpt_model={}, language={}, personality={}, personality_type={})".format(
            repr("Ceres Fauna"),
            18,
            repr("gpt-4"),
            repr(CeresFauna.language),
            repr(CeresFauna.personality),
            repr(CeresFauna.personality_type),
        )
        self.logger.debug("Expected: {}".format(expected))

        self.assertEqual(repr(vtuber), expected)
        self.logger.info("Tested the __repr__ method of the CeresFauna class.")


if __name__ == "__main__":
    unittest.main()
