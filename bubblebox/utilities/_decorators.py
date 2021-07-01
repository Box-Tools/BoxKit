"""Module with implementation of decorators"""

import joblib
import functools
import os

def blockparallel(target):
    """
    Decorator to parallelize a function operating on a block
    using joblib   

    Parameters
    ----------
    target : function to parallelize - operates on a block
             ['NUMEXPR_NUM_THREADS']
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

        Number of parallel tasks - ntasks - are inferred from the
        environment variable 'BUBBLEBOX_NTASKS_BLOCKS'

        ntasks = 1 or None reverts to serial mode
        """

        ntasks  = int(os.getenv('BUBBLEBOX_NTASKS_BLOCKS') or 1)

        with joblib.parallel_backend('loky'):
            listresult = joblib.Parallel(n_jobs=ntasks)(
                             joblib.delayed(target)(block,*args) for block in blocklist)

        return listresult

    return parallel_wrapper

def regionparallel(target):
    """
    Decorator to parallelize a function operating on a region
    using joblib   

    Parameters
    ----------
    target : function to parallelize - operates on a region
             
             def target(region, *args)

             actual call passes regionframes
      
             target(regionframes, *args)
    """

    @functools.wraps(target)
    def parallel_wrapper(progress,regionframes,*args): #TODO - find a better way to measure progress
        """
        Wrapper takes in regionframes and additional arguments and
        then applies target operations to individual regions in 
        parallel

        Number of parallel tasks - ntasks - are inferred from the
        environment variable 'BUBBLEBOX_NTASKS_REGIONS'

        ntasks = 1 or None reverts to serial mode
        """

        ntasks  = int(os.getenv('BUBBLEBOX_NTASKS_REGIONS') or 1)

        with joblib.parallel_backend('loky'):
            listresult = joblib.Parallel(n_jobs=ntasks)(
                             joblib.delayed(target)(region,*args) for region in regionframes if not progress.next())

        return listresult

    return parallel_wrapper
