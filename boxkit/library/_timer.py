"""Module with implementation of the Timer class."""

import time


class Timer:
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
        print("%s: %.3fs" % (self.name, self.time))
