"""Module with implemenation of utilities backend"""

import os
import sys
import ctypes
import bubblebox

from progress.bar import FillingSquaresBar as Bar

libname = "../build/libbubblebox.a"
libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + libname
bubbleboxlib = ctypes.cdll.LoadLibrary(libpath)

def exectask(action,unitlist,*args):
    """
    Parameters
    ----------
    action   : action object contains following attributes

             target : function/action operates on an unit ---> def target(unit, *args)
                      actual call passes unitlist ---> target(unitlist, *args)

             nthreads : number of nthreads (only relevant for parallel operations)

             monitor  : flag (True or False) to show progress bar for action

    unitlist : list of units

    args : tuple of additional arguments

    """
    if type(action) is not bubblebox.utilities.Action:
        raise ValueError('[boxlib.utilities.ExecuteTask] Type mismatch in action,'+
                         'expected "{}" got "{}"'.format(bubblebox.utilities.Action,action))

    if(type(unitlist) is not list):
        raise ValueError('[boxlib.utilities.ExecuteTask] unitlist must be a list of units')

    for unit in unitlist:
        if(type(unit) is not action.unit): 
            raise ValueError('[boxlib.utilities.ExecuteTask] Unit type not consistent.' +
                             'Expected "{}" but got "{}"'.format(action.unit,type(unit)))

    action.nthreads = action.nthreads or 1

    backends = {'boxlib' : _pytask_wrapper}

    return backends[action.backend](action,unitlist,*args)

def _pytask_wrapper(action,unitlist,*args):
    """
    Wrapper takes in unitlist and additional arguments and
    then applies target operations to individual units using boxlib
    """    
    bubbleboxlib.utilities_executePyTask.argtypes = [ctypes.py_object]*4
    bubbleboxlib.utilities_executePyTask.restype  = ctypes.py_object

    if(action.monitor):
        progressBar = Bar('',max=len(unitlist),suffix = '%(percent)d%%')

    else:
        progressBar = None

    listresult = bubbleboxlib.utilities_executePyTask(progressBar,action,unitlist,args)


    return listresult
