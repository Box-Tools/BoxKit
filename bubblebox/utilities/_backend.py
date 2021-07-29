"""Module with implementation of decorator utilities"""

import joblib
import functools
import os

from progress.bar import FillingSquaresBar as Bar

def backend(target=None,tasks=None,monitor=False,process='serial'):
    """
    Parameters
    ----------
    target : function/task operates on an unit ---> def target(unit, *args)
             actual call passes unitlist ---> target(unitlist, *args)

    tasks : number of tasks (only relevant for parallel operations)

    monitor : flag (True or False) to show progress bar for task

    process : 'serial', 'parallel'
    """
    @functools.wraps(target)
    def serial_wrapper(unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        serial
        """
        if monitor:
            bar = Bar('run-serial:'+target.__module__+'.'+target.__name__,max=len(unitlist),
                      suffix = '%(percent)d%%')
            listresult = [target(unit,*args) for unit in unitlist if not bar.next()]
            bar.finish()
        else:
            listresult = [target(unit,*args) for unit in unitlist]
        return listresult

    @functools.wraps(target)
    def parallel_wrapper(unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        parallel

        tasks = 1 or None reverts to serial mode
        """
        if monitor:
            bar = Bar('run-loky-parallel:'+target.__module__+'.'+target.__name__,max=len(unitlist),
                      suffix = '%(percent)d%%')
            listresult = joblib.Parallel(n_jobs=tasks,backend="loky")(
                             joblib.delayed(target)(unit,*args) for unit in unitlist 
                                                                      if not bar.next())
            bar.finish()
        else:
            listresult = joblib.Parallel(n_jobs=tasks,backend="loky")(
                             joblib.delayed(target)(unit,*args) for unit in unitlist) 

        return listresult

    tasks = tasks or 1

    if process == 'serial':
        return serial_wrapper

    elif process == 'parallel':
        return parallel_wrapper
