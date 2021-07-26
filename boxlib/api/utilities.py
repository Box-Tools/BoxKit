"""Module with implemenation of utilities backend"""

import os
import sys
import ctypes
import progress

libname = "../src/libbubblebox.a"
libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + libname
boxlib  = ctypes.cdll.LoadLibrary(libpath)

def parallel_wrapper(bar,ntasks,target,objectlist,*args):
    """
    Parallel wrapper

    Arguments:
    ----------
    bar : progress bar object

    ntasks : num tasks

    target : target function

    objectlist : list of objects

    Returns:
    --------
    listresult : list of result

    """
    boxlib.parallel_wrapper_pyobj.argtypes = [ctypes.py_object,ctypes.c_int,
                                              ctypes.py_object,ctypes.py_object,ctypes.py_object]

    boxlib.parallel_wrapper_pyobj.restype  = ctypes.py_object

    listresult = boxlib.parallel_wrapper_pyobj(bar,ntasks,target,objectlist,args)

    return listresult
