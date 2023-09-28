import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):
    def __init__(self, function=None):
        self.function = function
        self.last_event_time = 0

    def on_any_event(self, event):
        if (
            event.event_type == "modified"
            and event.src_path.endswith("transcript.txt")
            and time.time() - self.last_event_time > 1
        ):
            self.last_event_time = time.time()
            if self.function is not None:
                self.function(event)
        # else:
            # print(f"{event.event_type}:{event}")  # Your code here


if __name__ == "__main__":
    watcher = Watcher(".", MyHandler())
    watcher.run()
