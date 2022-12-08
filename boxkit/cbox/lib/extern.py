"""Module for cbox extern interface"""

import os
import ctypes
import sys

# Set path for file directory
_libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

# Load modules
_modulelist = ["library"]
for _module in _modulelist:
    setattr(
        sys.modules[__name__],
        _module,
        ctypes.cdll.LoadLibrary(_libpath + _module + ".so"),
    )
