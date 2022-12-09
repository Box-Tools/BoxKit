"""Module with implemenetation of api reshape methods"""

import math

from .. import library

from ..resources import stencils

from ..library import Timer


def Filterblocks(
    dataset, varlist=None, level=1, nthreads=1, monitor=False, backend="serial"
):
    """
    Build a pseudo UG dataset from AMR dataset at a level
    """
    if not varlist:
        varlist = dataset.varlist

    elif isinstance(varlist, str):
        varlist = [varlist]

    pass


def Mergeblocks(dataset, varlist, level=1, nthreads=1, monitor=False, backend="serial"):
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

    merged_data = library.Data(
        nblocks=1,
        nxb=nblockx * dataset.nxb,
        nyb=nblocky * dataset.nyb,
        nzb=nblockz * dataset.nzb,
    )

    merged_blocklist = [
        library.Block(
            merged_data,
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

    merged_dataset = library.Dataset(merged_blocklist, merged_data)

    blocklist_sorted = [None] * len(blocklist_level)

    for block in blocklist_level:
        iloc, jloc, kloc = block.get_location(
            origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
        )

        # TODO - this statement behaves differently for
        # test datasets vs logical way - investigate. It maybe because
        # test datasets were not constructured properly and maybe its time
        # to build a new test datasets after all
        #
        # for test data
        # blocklist_sorted[kloc + nblockx * jloc + nblockx * nblocky * iloc] = block
        #
        # desired
        blocklist_sorted[iloc + nblockx * jloc + nblockx * nblocky * kloc] = block

    for varkey in varlist:
        merged_dataset.addvar(varkey, dtype=dataset._data.dtype[varkey])

        stencils.reshape.map_blk_to_merged_dset.nthreads = nthreads
        stencils.reshape.map_blk_to_merged_dset.monitor = monitor
        stencils.reshape.map_blk_to_merged_dset.backend = backend

        time_mapping = Timer("[boxkit.stencils.map_dataset_block]")
        stencils.reshape.map_blk_to_merged_dset(
            blocklist_sorted, merged_dataset, varkey
        )
        del time_mapping

    del time_mergeblocks
    return merged_dataset
