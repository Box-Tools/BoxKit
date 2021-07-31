"""Module with implementation of Backend utility"""

import functools
import os

import joblib
from tqdm import tqdm

import dask
from dask.distributed import Client, progress

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
        if(monitor): unitlist = tqdm(unitlist)

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
        if(monitor): unitlist = tqdm(unitlist)

        listresult = joblib.Parallel(n_jobs=nthreads,backend="loky")(
                         joblib.delayed(target)(self,unit,*args) for unit in unitlist) 

        return listresult

    @functools.wraps(target)
    def dask_wrapper(self,unitlist,*args):
        """
        Wrapper takes in unitlist and additional arguments and
        then applies target operations to individual units in 
        using dask parallel backend

        nthreads = 1 or None reverts to serial mode
        """
        client = Client(threads_per_worker=nthreads,n_workers=1,processes=False)

        #if monitor: unitlist = tqdm(unitlist)
        #lazy_results = [dask.delayed(target)(self,unit,*args) for unit in unitlist]
        #futures = dask.persist(*lazy_results)
        #listresult = dask.compute(*futures)

        biglist = client.scatter(unitlist)
        futures = client.map(target, [self]*len(biglist), biglist, 
                                    *[[arg]*len(biglist) for arg in args]) 

        if(monitor): progress(futures)

        listresult = client.gather(futures)

        return listresult

    nthreads = nthreads or 1

    backends = {'serial' : serial_wrapper,
                'loky'   : loky_wrapper,
                'dask'   : dask_wrapper}

    if(monitor): print('run-'+label+':'+target.__module__+'.'+target.__name__)

    return backends[label]
