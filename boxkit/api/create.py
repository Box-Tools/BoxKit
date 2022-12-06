"""Module with implemenetation of api create methods"""

import time
import math

from .. import library

from ..library.utilities import Action


def dataset(data_attributes={}, block_attributes=[{}], storage="numpy-memmap"):
    """
    Create a dataset from a file

    Parameters
    ----------
    data_attributes  : data attributes
    block_attributes : block attributes
    storage          : storage option 'disk', 'pyarrow', or 'dask'
                       default('disk')

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """
    data = library.create.Data(storage=storage, **data_attributes)

    blocklist = [
        library.create.Block(data, **attributes) for attributes in block_attributes
    ]

    return library.create.Dataset(blocklist, data)


@Action(unit=library.create.Block, backend="loky")
def _reshape_block(self, unit, dataset_reshaped, varkey):
    iloc, jloc, kloc = [
        math.ceil(
            (unit.xmin - dataset_reshaped.xmin) / (unit.xmax - unit.xmin + 1e-13)
        ),
        math.ceil(
            (unit.ymin - dataset_reshaped.ymin) / (unit.ymax - unit.ymin + 1e-13)
        ),
        math.ceil(
            (unit.zmin - dataset_reshaped.zmin) / (unit.zmax - unit.zmin + 1e-13)
        ),
    ]

    dataset_reshaped[varkey][
        0,
        unit.nxb * iloc : unit.nxb * (iloc + 1),
        unit.nyb * jloc : unit.nyb * (jloc + 1),
        unit.nzb * kloc : unit.nzb * (kloc + 1),
    ] = unit[varkey][:, :, :]


def reshaped_dataset(dataset, varlist, level=1, nthreads=1):
    """
    Reshaped dataset at a level
    """
    if isinstance(varlist, str):
        varlist = [varlist]

    level_dx, level_dy, level_dz = [None] * 3

    blocklist_level = []

    for block in dataset.blocklist:
        if block.level == level:
            blocklist_level.append(block)

    if not blocklist_level:
        raise ValueError(
            f"[boxkit.library.dataset]: level={level} does not exist in input dataset"
        )

    region_level = library.create.Region(blocklist_level)

    nblockx = int((dataset.xmax - dataset.xmin) / blocklist_level[0].dx / dataset.nxb)
    nblocky = int((dataset.ymax - dataset.ymin) / blocklist_level[0].dy / dataset.nyb)
    nblockz = int((dataset.zmax - dataset.zmin) / blocklist_level[0].dz / dataset.nzb)

    if nblockx == 0:
        nblockx = 1

    if nblocky == 0:
        nblocky = 1

    if nblockz == 0:
        nblockz = 1

    data_reshaped = library.create.Data(
        nblocks=1,
        nxb=nblockx * dataset.nxb,
        nyb=nblocky * dataset.nyb,
        nzb=nblockz * dataset.nzb,
    )

    blocklist_reshaped = [
        library.create.Block(
            data_reshaped,
            dx=blocklist_level[0].dx,
            dy=blocklist_level[0].dy,
            dz=blocklist_level[0].dz,
            xmin=region_level.xmin,
            ymin=region_level.ymin,
            zmin=region_level.zmin,
            xmax=region_level.xmax,
            ymax=region_level.ymax,
            zmax=region_level.zmax,
        )
    ]

    dataset_reshaped = library.create.Dataset(blocklist_reshaped, data_reshaped)

    for varkey in varlist:
        dataset_reshaped.addvar(varkey, dtype=dataset._data.dtype[varkey])

        _reshape_block.nthreads = nthreads
        _reshape_block.monitor = True
        _reshape_time = time.time()
        _reshape_block(blocklist_level, dataset_reshaped, varkey)
        _reshape_time = time.time() - _reshape_time

        print("[boxkit.api.create] reshapping time: ", _reshape_time)

    return dataset_reshaped


def region(dataset, **attributes):
    """
    Create a region from a dataset

    Parameters
    ----------
    dataset    : Dataset object
    attributes : dictionary of attributes
                 { 'xmin' : low x bound
                   'ymin' : low y bound
                   'zmin' : low z bound
                   'xmax' : high x bound
                   'ymax' : high y bound
                   'zmax' : high z bound }
    Returns
    -------
    Region object
    """

    region_attributes = {
        "xmin": dataset.xmin,
        "ymin": dataset.ymin,
        "zmin": dataset.zmin,
        "xmax": dataset.xmax,
        "ymax": dataset.ymax,
        "zmax": dataset.zmax,
    }

    for key, value in attributes.items():
        region_attributes[key] = value

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.create.Region(blocklist, **region_attributes)


def slice(dataset, **attributes):
    """
    Create a slice from a dataset

    Parameters
    ----------
    dataset    : Dataset object
    attributes : dictionary of attributes
                 { 'xmin' : low x bound
                   'ymin' : low y bound
                   'zmin' : low z bound
                   'xmax' : high x bound
                   'ymax' : high y bound
                   'zmax' : high z bound }

    Returns
    -------
    Slice object
    """

    slice_attributes = {
        "xmin": dataset.xmin,
        "ymin": dataset.ymin,
        "zmin": dataset.zmin,
        "xmax": dataset.xmax,
        "ymax": dataset.ymax,
        "zmax": dataset.zmax,
    }

    for key, value in attributes.items():
        slice_attributes[key] = value

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.create.Slice(blocklist, **slice_attributes)
