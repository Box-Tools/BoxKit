import os
import ctypes
import sys

_libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

_modulelist = ["utilities"]

for _module in _modulelist:
    setattr(sys.modules[__name__],_module,ctypes.cdll.LoadLibrary(_libpath + _module + ".so"))
