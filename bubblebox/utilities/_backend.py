"""Module with implementation of decorator utilities"""

import joblib
import functools
import os

from progress.bar import FillingSquaresBar as Bar

def Backend(target=None,nthreads=None,monitor=False,backend_wrapper='serial'):
    """
    Parameters
    ----------
    target : function/task operates on an unit ---> def target(unit, *args)
             actual call passes unitlist ---> target(unitlist, *args)

    nthreads : number of nthreads (only relevant for parallel operations)

    monitor : flag (True or False) to show progress bar for task

    backend_wrapper : 'serial', 'parallel'
    """
    @functools.wraps(target)
    def serial_wrapper(self,unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        serial
        """
        if monitor:
            bar = Bar('run-serial:'+target.__module__+'.'+target.__name__,max=len(unitlist),
                      suffix = '%(percent)d%%')
            listresult = [target(self,unit,*args) for unit in unitlist if not bar.next()]
            bar.finish()
        else:
            listresult = [target(self,unit,*args) for unit in unitlist]
        return listresult

    @functools.wraps(target)
    def parallel_wrapper(self,unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        parallel

        nthreads = 1 or None reverts to serial mode
        """
        if monitor:
            bar = Bar('run-loky-parallel:'+target.__module__+'.'+target.__name__,max=len(unitlist),
                      suffix = '%(percent)d%%')
            listresult = joblib.Parallel(n_jobs=nthreads,backend="loky")(
                             joblib.delayed(target)(self,unit,*args) for unit in unitlist 
                                                                      if not bar.next())
            bar.finish()
        else:
            listresult = joblib.Parallel(n_jobs=nthreads,backend="loky")(
                             joblib.delayed(target)(self,unit,*args) for unit in unitlist) 

        return listresult

    nthreads = nthreads or 1

    wrapper_dict = {'serial'   : serial_wrapper,
                    'parallel' : parallel_wrapper};

    return parallel_wrapper
