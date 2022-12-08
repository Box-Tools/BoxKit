""" Module with implemenation of region methods"""

import itertools
import numpy

from .. import library
from ..library import Timer
from ..resources import stencils

from . import create
from . import reshape


def Regionprops(dataset, lsetkey, backend="serial", nthreads=1, monitor=False):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    dataset : Dataset object
    lsetkey : key containing level-set/binary data

    Returns
    -------
    listprops : list of bubble properties
    """

    labelkey = "bwlabel"
    dataset.addvar(labelkey, dtype=int)

    region = create.Region(dataset)

    stencils.regionprops_block.nthreads = nthreads
    stencils.regionprops_block.backend = backend
    stencils.regionprops_block.monitor = monitor

    listprops = stencils.regionprops_block(region.blocklist, lsetkey, labelkey)
    listprops = list(itertools.chain.from_iterable(listprops))

    dataset.delvar(labelkey)

    return listprops


def Average(datasets, varlist, level=1, backend="serial", nthreads=1, monitor=False):
    """
    Compute average across a dataset list
    """
    time_average = Timer("[boxkit.measure.average]")

    if isinstance(varlist, str):
        varlist = [varlist]

    reshaped_datasets = [
        reshape.Mergeblocks(dataset, varlist, level=level, monitor=monitor)
        for dataset in datasets
    ]

    nxb, nyb, nzb, dx, dy, dz, xmin, ymin, zmin, xmax, ymax, zmax = [
        reshaped_datasets[0].nxb,
        reshaped_datasets[0].nyb,
        reshaped_datasets[0].nzb,
        reshaped_datasets[0].blocklist[0].dx,
        reshaped_datasets[0].blocklist[0].dy,
        reshaped_datasets[0].blocklist[0].dz,
        reshaped_datasets[0].xmin,
        reshaped_datasets[0].ymin,
        reshaped_datasets[0].zmin,
        reshaped_datasets[0].xmax,
        reshaped_datasets[0].ymax,
        reshaped_datasets[0].zmax,
    ]

    for dataset in reshaped_datasets:
        if [nxb, nyb, nzb] != [dataset.nxb, dataset.nyb, dataset.nzb]:
            raise ValueError("[boxkit.measure.average] inconsistent sizes for datasets")

    average_data = library.Data(nblocks=1, nxb=nxb, nyb=nyb, nzb=nzb)

    average_blocklist = [
        library.Block(
            average_data,
            dx=dx,
            dy=dy,
            dz=dz,
            xmin=xmin,
            ymin=ymin,
            zmin=zmin,
            xmax=xmax,
            ymax=ymax,
            zmax=zmax,
        )
    ]

    average_dataset = library.Dataset(average_blocklist, average_data)

    for varkey in varlist:
        average_dataset.addvar(varkey)

        time_atomic = Timer("[boxkit.measure.average atomic]")
        for dataset in reshaped_datasets:
            average_dataset[varkey][:] = dataset[varkey][:] / len(reshaped_datasets)
        del time_atomic

    for dataset in reshaped_datasets:
        dataset.purge("boxmem")

    del time_average
    return average_dataset
