"""Module with implemenetation of api reshape methods"""

from .. import library
from .. import api


def resfilter(
    dataset, varlist=None, level=1, nthreads=1, monitor=False, backend="serial"
):
    """
    Build a pseudo UG dataset from AMR dataset at a level

    Arguments
    ---------
    dataset  - BoxKit library Dataset
    varlist  - list of variables to filter
    level    - AMR level default is 1
    nthreads - number of threads to run this operation on
    monitor  - flag for timer and indicator for process
    backend  - backend

    Returns
    -------
    filtered_dataset - BoxKit library Dataset

    """
    if monitor:
        time_resfilter = library.Timer("[boxkit.resfilter]")

    if not varlist:
        varlist = dataset.varlist

    elif isinstance(varlist, str):
        varlist = [varlist]

    for block in dataset.blocklist:
        if block.level == level:
            dx_level, dy_level, dz_level = [block.dx, block.dy, block.dz]
            break

        raise ValueError(
            f"[boxkit.resfilter]: level={level} does not exist in input dataset"
        )

    nblockx_level = int((dataset.xmax - dataset.xmin) / dx_level / dataset.nxb)
    nblocky_level = int((dataset.ymax - dataset.ymin) / dy_level / dataset.nyb)
    nblockz_level = int((dataset.zmax - dataset.zmin) / dz_level / dataset.nzb)

    nblockx_level, nblocky_level, nblockz_level = [
        value if value > 0 else 1
        for value in [nblockx_level, nblocky_level, nblockz_level]
    ]

    filtered_dataset = api.create_dataset(
        nblockx=nblockx_level,
        nblocky=nblocky_level,
        nblockz=nblockz_level,
        nxb=dataset.nxb,
        nyb=dataset.nyb,
        nzb=dataset.nzb,
        xmin=dataset.xmin,
        ymin=dataset.ymin,
        zmin=dataset.zmin,
        xmax=dataset.xmax,
        ymax=dataset.ymax,
        zmax=dataset.zmax,
    )

    if monitor:
        del time_resfilter
