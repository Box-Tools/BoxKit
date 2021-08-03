"""Module with implementation of Backend utility"""

import functools
import os

import joblib
import tqdm
import dask

import dask.distributed as distributed

def Backend(target=None,nthreads=None,monitor=False,label='serial'):
    """
    Parameters
    ----------
    target       : function/task operates on an unit ---> def target(unit, *args)
                   actual call passes unitlist ---> target(unitlist, *args)

    nthreads     : number of nthreads (only relevant for parallel operations)

    monitor_flag : flag (True or False) to show progress bar for task

    backend_key  : 'serial', 'loky', 'dask'
    """
    @functools.wraps(target)
    def serial_wrapper(self,unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        serial
        """
        if(monitor): unitlist = tqdm.tqdm(unitlist)

        listresult = [target(self,unit,*args) for unit in unitlist]

        return listresult

    @functools.wraps(target)
    def loky_wrapper(self,unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        parallel using joblib "loky" backend

        nthreads = 1 or None reverts to serial mode
        """
        if(monitor): unitlist = tqdm.tqdm(unitlist)

        with joblib.parallel_backend(n_jobs=nthreads,backend="loky"):

            listresult = joblib.Parallel()(joblib.delayed(target)(self,unit,*args) for unit in unitlist) 

        return listresult

    @functools.wraps(target)
    def dask_wrapper(self,unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        using dask parallel backend

        nthreads = 1 or None reverts to serial mode
        """
        with distributed.LocalCluster(threads_per_worker=nthreads, 
                                      n_workers=None,
                                      processes=False) as cluster, distributed.Client(cluster) as client:

            #if monitor: unitlist = tqdm.tqdm(unitlist)
            #lazy_results = [dask.delayed(target)(self,unit,*args) for unit in unitlist]
            #futures = dask.persist(*lazy_results)
            #listresult = dask.compute(*futures)

            biglist = client.scatter(unitlist)
            futures = client.map(target, [self]*len(biglist), biglist, 
                                        *[[arg]*len(biglist) for arg in args]) 
            
            if(monitor): distributed.progress(futures)
            
            listresult = client.gather(futures)

        return listresult

    nthreads = nthreads or 1

    backends = {'serial' : serial_wrapper,
                'loky'   : loky_wrapper,
                'dask'   : dask_wrapper}

    if(monitor): print('run-'+label+':'+target.__module__+'.'+target.__name__)

    return backends[label]
