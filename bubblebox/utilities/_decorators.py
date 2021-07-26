"""Module with implementation of decorator utilities"""

import boxlib.api as boxapi
import joblib
import functools
import os

from progress.bar import FillingSquaresBar as Bar

def serial(target):
    """
    Decorator to serially execute a function operating on an object

    Parameters
    ----------
    target : function to parallelize - operates on an object
             
             def target(object, *args)

             actual call passes objectlist
      
             target(objectlist, *args)
    """
    @functools.wraps(target)
    def serial_wrapper(objectlist,*args):
        """
        Wrapper takes in objectlist and additional arguments and
        then applies target operations to individual objects in 
        serial
        """
        listresult = [target(object,*args) for object in objectlist]
        return listresult
    return serial_wrapper

def parallel(target=None,backend='loky'):
    """
    Decorator to parallelize a function operating on an object
    using joblib   

    Parameters
    ----------
    target : function to parallelize - operates on an object
             
             def target(object, *args)

             actual call passes objectlist
      
             target(objectlist, *args)

    backend : 'loky'
            : 'boxlib'
    """
    def parallel_decorator(target):
        """
        Arguments:
        ----------
        target : function to parallelize

        """
        @functools.wraps(target)
        def parallel_wrapper(objectlist,*args): #TODO remove progress
            """
            Wrapper takes in objectlist and additional arguments and
            then applies target operations to individual objects in 
            parallel

            Number of parallel tasks - ntasks - are inferred from the
            environment variable 'BUBBLEBOX_NTASKS_PARALLEL'

            ntasks = 1 or None reverts to serial mode
            """
            ntasks  = int(os.getenv('BUBBLEBOX_NTASKS_PARALLEL') or 1)

            bar = Bar('run-parallel:'+target.__module__+'.'+target.__name__,max=len(objectlist),
                      suffix = '%(percent)d%%')

            if backend == 'loky':
                listresult = joblib.Parallel(n_jobs=ntasks,backend='loky')(
                                 joblib.delayed(target)(object,*args) for object in objectlist 
                                                                       if not bar.next())

            elif backend == 'boxlib':
                listresult = boxapi.utilities.parallel_wrapper(bar,ntasks,target,objectlist,*args)

            bar.finish()

            return listresult

        return parallel_wrapper

    if target:
        return parallel_decorator(target)

    else:
        return parallel_decorator
