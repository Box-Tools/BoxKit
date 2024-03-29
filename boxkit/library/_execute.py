"""Module with implementation of ExecuteTask utility"""

from types import SimpleNamespace

import joblib
import tqdm

from boxkit import options

if options.DASK:
    import dask  # pylint: disable=unused-import
    from dask import distributed

if options.CBOX:
    import ctypes  # pylint: disable=unused-import
    from ..cbox.lib import extern as cbox  # pylint: disable=unused-import


def exectask(action, obj_list, *args, **kwargs):
    """
    Parameters
    ----------
    action   : action object contains following attributes

               target   : function/action operates on a,
                          parallel_obj ---> def target(parallel_obj, args)

                          actual call passes,
                          obj_list ---> target(obj_list, args)

               nthreads : number of nthreads (only relevant for parallel operations)
               monitor  : flag (True or False) to show progress bar for action
               backend  : 'serial', 'loky', 'dask'

    obj_list : list of parallel_objs

    args : tuple of additional arguments

    """
    action.nthreads = action.nthreads or 1

    self = SimpleNamespace()
    self.backends = {
        "serial": execute_serial,
        "loky": execute_loky,
        "dask": execute_dask,
        "cbox": execute_cbox,
    }

    if action.monitor:
        print(
            "run-"
            + action.backend
            + ":"
            + action.target.__module__
            + "."
            + action.target.__name__
        )

    return self.backends[action.backend](action, obj_list, *args, **kwargs)


def execute_serial(action, obj_list, *args, **kwargs):
    """
    Wrapper takes in obj_list and additional arguments and
    then applies target operations to individual parallel_objs in
    serial
    """
    if action.monitor:
        obj_list = tqdm.tqdm(obj_list)

    listresult = [
        action.target(parallel_obj, *args, **kwargs) for parallel_obj in obj_list
    ]

    return listresult


def execute_loky(action, obj_list, *args, **kwargs):
    """
    Wrapper takes in obj_list and additional arguments and
    then applies target operations to individual parallel_objs in
    parallel using joblib "loky" backend

    nthreads = 1 or None reverts to serial mode
    """
    if action.monitor:
        obj_list = tqdm.tqdm(obj_list)

    with joblib.parallel_backend(n_jobs=action.nthreads, backend="loky"):
        listresult = joblib.Parallel(batch_size=action.batch)(
            joblib.delayed(action.target)(parallel_obj, *args, **kwargs)
            for parallel_obj in obj_list
        )

    return listresult


def execute_cbox(action, obj_list, *args, **kwargs):
    """
    Wrapper takes in obj_list and additional arguments and
    then applies target operations to individual parallel_objs using boxlib
    """
    # if options.CBOX:
    #    cbox.utilities.execute_pyTask.argtypes = [ctypes.py_object] * 3
    #    cbox.utilities.execute_pyTask.restype = ctypes.py_object
    #
    #    listresult = cbox.library.execute_pyTask(action, obj_list, args)
    #    return listresult
    # else:
    #    raise NotImplementedError(
    #        "[boxkit.library.execute) Install --with-cbox to use CBOX backend"
    #    )

    raise NotImplementedError("[boxkit.library.execute] CBOX backend not implemented")


def execute_dask(action, obj_list, *args, **kwargs):
    """
    Wrapper takes in obj_list and additional arguments and
    then applies target operations to individual parallel_objs in
    using dask parallel backend

    nthreads = 1 or None reverts to serial mode
    """
    if options.DASK:
        with distributed.LocalCluster(
            threads_per_worker=None, n_workers=None, processes=False
        ) as cluster, distributed.Client(cluster) as client:

            # --------------METHOD 1---------------------------
            # if(action.monitor): obj_list = tqdm.tqdm(obj_list)
            # lazy_results = [dask.delayed(action.target)(parallel_obj,*args, **kwargs)
            #                 for parallel_obj in obj_list]
            # futures = dask.persist(*lazy_results)
            # listresult = dask.compute(*futures)

            # --------------METHOD 2---------------------------
            biglist = client.scatter(obj_list)
            futures = client.map(
                action.target,
                biglist,
                *[[arg] * len(biglist) for arg in args],
                **kwargs,
            )

            if action.monitor:
                distributed.progress(futures)

            listresult = client.gather(futures)

            # --------------METHOD 3---------------------------
            # if action.monitor:
            #     obj_list = tqdm.tqdm(obj_list)

            # with joblib.parallel_backend(n_jobs=action.nthreads, backend="dask"):
            #     listresult = joblib.Parallel(batch_size=action.batch)(
            #         joblib.delayed(action.target)(parallel_obj, *args, **kwargs)
            #         for parallel_obj in obj_list
            #     )

            return listresult

    else:
        raise NotImplementedError(
            "[boxkit.library.execute] Install --with-dask to use DASK backend"
        )
