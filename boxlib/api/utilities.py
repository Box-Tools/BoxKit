"""Module with implemenation of utilities backend"""

import os
import sys
import ctypes
import progress

libname = "../build/libbubblebox.a"
libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + libname
bubbleboxlib = ctypes.cdll.LoadLibrary(libpath)

def parallel_wrapper(target,objectlist,args,bar,ntasks):
    """
    Parallel wrapper

    Arguments:
    ----------
    target : target function

    objectlist : list of objects

    args : tuple of additional arguments

    bar : progress bar object

    ntasks : num tasks

    Returns:
    --------
    listresult : list of result

    """
    bubbleboxlib.Parallel_PyWrapper.argtypes = [ctypes.py_object,ctypes.py_object,ctypes.py_object,
                                          ctypes.py_object,ctypes.c_int]

    bubbleboxlib.Parallel_PyWrapper.restype  = ctypes.py_object

    listresult = bubbleboxlib.Parallel_PyWrapper(target,objectlist,args,bar,ntasks)

    return listresult
