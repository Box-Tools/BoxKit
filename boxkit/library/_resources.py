"""Module for managing resources"""

from collections import namedtuple
import psutil

def Resources():
    """
    Return dictionary of available and used resources to optimize usage
    """
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_used": psutil.cpu_percent()*psutil.cpu_count()/100,
        "cpu_percent": psutil.cpu_percent(),
        "mem_percent": psutil.virtual_memory()[2], 
    }


if __name__ == "__main__":
    resources = Resources()
    print(resources["cpu_count"], resources["cpu_used"], resources["cpu_percent"], resources["mem_percent"])
