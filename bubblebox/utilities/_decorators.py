"""Module with implementation of decorators"""

import joblib
import functools
import itertools
import os

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
    def parallel_wrapper(objectlist,*args):
        """
        Wrapper takes in objectlist and additional arguments and
        then applies target operations to individual objects in 
        parallel

        Number of parallel tasks - npool - are inferred from the
        environment variable 'BUBBLEBOX_NPOOL_BACKEND'


        npool = 1 or None reverts to serial mode
        """

        npool = int(os.getenv('BUBBLEBOX_NPOOL_BACKEND') or 1)

        listresult = joblib.Parallel(n_jobs=npool)(        
                         joblib.delayed(target)(object,*args) for object in objectlist)

        return listresult

    return parallel_wrapper
