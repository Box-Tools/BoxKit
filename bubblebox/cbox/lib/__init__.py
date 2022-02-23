import os
import ctypes
from distutils.sysconfig import get_python_version

# Set path to Boost library within the package
# This is needed when CBox is compiled using
# Boost built locally within the package
LOCAL_BOOST_PATH = (
    os.path.dirname(os.path.abspath(__file__))
    + os.path.sep
    + f"../../depends/boost/lib"
    + os.path.sep
)


_list_library = ["_python"]

# Load library if LOCAL_BOOST_PATH
# exists
if os.path.exists(LOCAL_BOOST_PATH):
    for _library in _list_library:
        ctypes.cdll.LoadLibrary(
            LOCAL_BOOST_PATH
            + "libboost"
            + _library
            + f'{"".join(get_python_version().split("."))}.so'
        )

# Import modules
from . import boost
from . import extern
