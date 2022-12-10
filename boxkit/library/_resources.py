"""Module for managing resources"""

import math
import psutil


def Resources():
    """
    Return dictionary of available and used resources to optimize usage
    """

    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent()
    virtual_memory = psutil.virtual_memory()

    return {
        "cpu_count": cpu_count,
        "cpu_avail": cpu_count - math.floor(cpu_percent * cpu_count / 100),
        "mem_avail": round(virtual_memory[1] / (2**30), 2),
        "cpu_usage": cpu_percent,
        "mem_usage": virtual_memory[2],
    }
