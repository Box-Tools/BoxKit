"""Module with implementation of decorator utilities"""

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

def parallel(target):
    """
    Decorator to parallelize a function operating on an object
    using joblib   

    Parameters
    ----------
    target : function to parallelize - operates on an object
             
             def target(object, *args)

             actual call passes objectlist
      
             target(objectlist, *args)

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

        lokyobjects = []

        for object in objectlist:

            if object.backend == "loky":
                lokyobjects.append(object)
           
            else:
                raise ValueError('Cannot implement backend "{}"'.format(object.backend))

        if lokyobjects: 

            lokytasks = int(os.getenv('BUBBLEBOX_LOKY_TASKS') or 1)

            bar = Bar('run-loky-parallel:'+target.__module__+'.'+target.__name__,max=len(lokyobjects),
                  suffix = '%(percent)d%%')

            lokyresult = joblib.Parallel(n_jobs=lokytasks,backend="loky")(
                           joblib.delayed(target)(object,*args) for object in lokyobjects 
                                                                if not bar.next())
            bar.finish()

        listresult = lokyresult

        return listresult
    return parallel_wrapper
