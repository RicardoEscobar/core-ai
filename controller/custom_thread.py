""""Custom Thread class to return value from thread.
Visit https://youtu.be/DPBm87pTByo?si=vmxQty6tCqsxEstE for more info."""

from threading import Thread

class CustomThread(Thread):
    """This custom thread class can be used to create threads that return a value when they complete. The return value can be retrieved by calling the join() method of the thread object. This can be useful in situations where you need to perform a long-running task in a separate thread and retrieve the result of the task when it completes."""
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None, daemon=False):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            
    def join(self, *args):
        Thread.join(self, *args)
        # super().join(*args)
        return self._return