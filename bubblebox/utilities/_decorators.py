"""Module with implementation of decorators"""

import joblib
import functools
import os

def blockparallel(target):
    """
    Decorator to parallelize a function operating on an block
    using joblib   

    Parameters
    ----------
    target : function to parallelize - operates on an block
             
             def target(block, *args)

             actual call passes blocklist
      
             target(blocklist, *args)
    """

    @functools.wraps(target)
    def parallel_wrapper(blocklist,*args):
        """
        Wrapper takes in blocklist and additional arguments and
        then applies target operations to individual blocks in 
        parallel

        Number of parallel tasks - npool - are inferred from the
        environment variable 'BUBBLEBOX_NPOOL_BACKEND'


        npool = 1 or None reverts to serial mode
        """

        npool = int(os.getenv('BUBBLEBOX_NPOOL_BACKEND') or 1)

        listresult = joblib.Parallel(n_jobs=npool)(
                         joblib.delayed(target)(block,*args) for block in blocklist)

        return listresult

    return parallel_wrapper
