import os
import ctypes
from distutils.sysconfig import get_python_version

# Load Boost Python
ctypes.cdll.LoadLibrary(
    os.path.dirname(os.path.abspath(__file__))
    + os.path.sep
    + f'../../depends/boost/lib/libboost_python{"".join(get_python_version().split("."))}.so'
)

# Import modules
from . import boost
from . import extern
