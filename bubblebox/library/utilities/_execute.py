"""Module with implementation of ExecuteTask utility"""

import joblib
import tqdm

import dask
import dask.distributed as distributed

import cbox.lib as cbox
import ctypes

def exectask(action,unitlist,*args):
    """
    Parameters
    ----------
    action   : action object contains following attributes

               target   : function/action operates on an unit ---> def target(unit, *args)
                          actual call passes unitlist ---> target(unitlist, *args)
               nthreads : number of nthreads (only relevant for parallel operations)
               monitor  : flag (True or False) to show progress bar for action
               backend  : 'serial', 'loky', 'dask'

    unitlist : list of units

    args : tuple of additional arguments

    """
    action.nthreads = action.nthreads or 1

    backends = {'serial' : serial_wrapper,
                'loky'   : loky_wrapper,
                'dask'   : dask_wrapper,
                'cbox'   : cbox_wrapper}

    if(action.monitor): print('run-'+action.backend+':'+action.target.__module__+'.'+action.target.__name__)

    return backends[action.backend](action,unitlist,*args)

def serial_wrapper(action,unitlist,*args):
    """
    Wrapper takes in unitlist and additional arguments and
    then applies target operations to individual units in 
    serial
    """
    if(action.monitor): unitlist = tqdm.tqdm(unitlist)

    listresult = [action.target(action,unit,*args) for unit in unitlist]

    return listresult

def loky_wrapper(action,unitlist,*args):
    """
    Wrapper takes in unitlist and additional arguments and
    then applies target operations to individual units in 
    parallel using joblib "loky" backend

    nthreads = 1 or None reverts to serial mode
    """
    if(action.monitor): unitlist = tqdm.tqdm(unitlist)

    with joblib.parallel_backend(n_jobs=action.nthreads,backend="loky"):
        listresult = joblib.Parallel()(joblib.delayed(action.target)(action,unit,*args) for unit in unitlist) 

    return listresult

def cbox_wrapper(action,unitlist,*args):
    """
    Wrapper takes in unitlist and additional arguments and
    then applies target operations to individual units using boxlib
    """    
    cbox.extern.utilities.executePyTask.argtypes = [ctypes.py_object]*3
    cbox.extern.utilities.executePyTask.restype  = ctypes.py_object

    listresult = cbox.extern.utilities.executePyTask(action,unitlist,args)

    return listresult

def dask_wrapper(action,unitlist,*args):
    """
    Wrapper takes in unitlist and additional arguments and
    then applies target operations to individual units in 
    using dask parallel backend

    nthreads = 1 or None reverts to serial mode
    """
    with distributed.LocalCluster(threads_per_worker=action.nthreads,
                                  n_workers=None,
                                  processes=False) as cluster, distributed.Client(cluster) as client:

        #if(action.monitor): unitlist = tqdm.tqdm(unitlist)
        #lazy_results = [dask.delayed(action.target)(action,unit,*args) for unit in unitlist]
        #futures = dask.persist(*lazy_results)
        #listresult = dask.compute(*futures)

        biglist = client.scatter(unitlist)
        futures = client.map(action.target, [action]*len(biglist), biglist, 
                                             *[[arg]*len(biglist) for arg in args]) 
            
        if(action.monitor): distributed.progress(futures)
            
        listresult = client.gather(futures)

    return listresult
