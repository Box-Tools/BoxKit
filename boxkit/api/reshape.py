"""Module with implemenetation of api reshape methods"""

import math

from .. import library

from ..resources import stencils

from ..library import Timer


def mergeblocks(dataset, varlist, level=1, nthreads=1, monitor=False, backend="serial"):
    """
    Reshaped dataset at a level
    """
    time_mergeblocks = Timer("[boxkit.reshape.mergeblocks]")

    if isinstance(varlist, str):
        varlist = [varlist]

    blocklist_level = []
    for block in dataset.blocklist:
        if block.level == level:
            blocklist_level.append(block)

    if not blocklist_level:
        raise ValueError(
            f"[boxkit.reshape.mergeblocks]: level={level} does not exist in input dataset"
        )

    dx_level, dy_level, dz_level = [
        blocklist_level[0].dx,
        blocklist_level[0].dy,
        blocklist_level[0].dz,
    ]

    region_level = library.Region(blocklist_level)

    nblockx = int((dataset.xmax - dataset.xmin) / dx_level / dataset.nxb)
    nblocky = int((dataset.ymax - dataset.ymin) / dy_level / dataset.nyb)
    nblockz = int((dataset.zmax - dataset.zmin) / dz_level / dataset.nzb)

    nblockx, nblocky, nblockz = [
        value if value > 0 else 1 for value in [nblockx, nblocky, nblockz]
    ]

    data_reshaped = library.Data(
        nblocks=1,
        nxb=nblockx * dataset.nxb,
        nyb=nblocky * dataset.nyb,
        nzb=nblockz * dataset.nzb,
    )

    blocklist_reshaped = [
        library.Block(
            data_reshaped,
            dx=dx_level,
            dy=dy_level,
            dz=dz_level,
            xmin=region_level.xmin,
            ymin=region_level.ymin,
            zmin=region_level.zmin,
            xmax=region_level.xmax,
            ymax=region_level.ymax,
            zmax=region_level.zmax,
        )
    ]

    dataset_reshaped = library.Dataset(blocklist_reshaped, data_reshaped)

    for varkey in varlist:
        dataset_reshaped.addvar(varkey, dtype=dataset._data.dtype[varkey])

        stencils.map_dataset_block.nthreads = nthreads
        stencils.map_dataset_block.monitor = monitor
        stencils.map_dataset_block.backend = backend

        time_mapping = Timer("[boxkit.stencils.map_dataset_block]")
        stencils.map_dataset_block(blocklist_level, dataset_reshaped, varkey)
        del time_mapping

    del time_mergeblocks
    return dataset_reshaped
