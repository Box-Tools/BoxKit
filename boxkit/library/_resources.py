"""Module for managing resources"""

import math
import psutil


class Resources: # pylint: disable=too-few-public-methods
    """
    Return dictionary of available and used resources to optimize usage
    """

    def __init__(self):
        """
        Constructor
        """
        self.cpu_count = psutil.cpu_count()
        self.cpu_usage = psutil.cpu_percent()
        self.virtual_memory = psutil.virtual_memory()
        self.cpu_avail = self.cpu_count - math.floor(
            self.cpu_usage * self.cpu_count / 100
        )
        self.mem_avail = round(self.virtual_memory[1] / (2**30), 2)
        self.mem_usage = self.virtual_memory[2]

    def display(self):
        """
        Display resource status
        """
        print(
            f"[cpu_count]: {self.cpu_count}",
            f"[cpu_avail]: {self.cpu_avail}",
            f"[mem_avail]: {self.mem_avail} GB",
            f"[cpu_usage]: {self.cpu_usage}%",
            f"[mem_usage]: {self.mem_usage}%",
        )
