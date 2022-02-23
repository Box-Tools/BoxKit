import os
import ctypes
from distutils.sysconfig import get_python_version

# Load Boost Python
LIB_BOOST_PATH = (
    os.path.dirname(os.path.abspath(__file__))
    + os.path.sep
    + f'../../depends/boost/lib/libboost_python{"".join(get_python_version().split("."))}.so'
)

if os.path.exists(LIB_BOOST_PATH):
    ctypes.cdll.LoadLibrary(LIB_BOOST_PATH)

# Import modules
from . import boost
from . import extern
