"""Module with implementation of decorators"""

import joblib
import functools
import os

def parallel(target):
    """
    Decorator to parallelize a function opearting on a block
    using joblib   

    Parameters
    ----------
    target : function to parallelize
    """

    @functools.wraps(target)
    def parallel_wrapper(blocklist,*args):
        """
        Wrapper takes in blocklist and additional arguments and
        then applies parallel block operations to target

        Number of parallel tasks - ntasks - are inferred from the
        environment variable 'BUBBLEBOX_NTASKS_BACKEND'


        ntasks = 1 reverts to serial mode        
        """

        ntasks = os.getenv('BUBBLEBOX_NTASKS_BACKEND')

        if ntasks: ntasks = int(ntasks)

        result = joblib.Parallel(n_jobs=ntasks)(        
                     joblib.delayed(target)(block,*args) for block in blocklist)

        return result

    return parallel_wrapper
