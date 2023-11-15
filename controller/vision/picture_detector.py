"""This module is for the eyes of the AI, the vision, the ability to see.
Detect the newly taken pictures and process them."""
# If this file is running alone, then add the root folder to the Python path
if __name__ == "__main__":
    import sys
    from pathlib import Path

    root_folder = Path(__file__).parent.parent.parent
    sys.path.append(str(root_folder))

import time
from pathlib import Path
import getpass
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from controller.vision.prepare_png import (
    resize_image_without_empty_space,
    crop_image_square,
    crop_image_vertical,
)
from controller.create_logger import create_logger

# Create a logger instance
log = create_logger(
    logger_name="controller.vision.picture_detector",
    logger_filename="picture_detector.log",
    log_directory="logs",
    console_logging=True,
    console_log_level=logging.INFO,
)

username = getpass.getuser()


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".png"):
            log.debug("New PNG file created: %s", event.src_path)
            latest_picture = (
                "./img/latest_picture_512x512.png"
            )
            if latest_picture != event.src_path:
                crop_image_square(event.src_path, latest_picture, size=512)


def watch_directory(path):
    # Create path if it doesn't exist
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    directory_to_watch = "./img"
    log.debug(f"Watching directory: {directory_to_watch}")
    watch_directory(directory_to_watch)
