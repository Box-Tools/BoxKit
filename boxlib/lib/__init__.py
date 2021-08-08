import os
import ctypes

libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

utilities = ctypes.cdll.LoadLibrary(libpath + "utilities.lib")
