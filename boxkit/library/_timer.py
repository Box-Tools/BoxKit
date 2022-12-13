"""Module with implementation of the Timer class."""

import time


class Timer:  # pylint: disable=too-few-public-methods
    """
    Timer class
    """

    def __init__(self, name):
        """
        Constructor
        """
        self.time = time.time()
        self.name = name

    def __del__(self):
        """
        Destructor
        """
        self.time = time.time() - self.time
        print(f"{self.name}: {round(self.time,3)}s")
