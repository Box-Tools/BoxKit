"""Module with implemenetation of api methods"""

import sys

from .. import library
from .. import api


def mergeblocks(dataset, varlist, level=1, nthreads=1, monitor=False, backend="serial"):
    """
    Reshaped dataset at a level
    """

    # Create a timer for the subroutine
    # and activate if monitor is True
    if monitor:
        time_mergeblocks = library.Timer("[boxkit.mergeblocks]")

    # Check if varlist is acutally a string
    # of one variable and convert to a list
    if isinstance(varlist, str):
        varlist = [varlist]

    # Compute list of blocks at level supplied
    # as a the function arguments
    blocklist_level = []
    for block in dataset.blocklist:
        if block.level == level:
            blocklist_level.append(block)

    # Handle errors
    if not blocklist_level:
        raise ValueError(
            f"[boxkit.mergeblocks]: level={level} does not exist in input dataset"
        )

    # Compute deltas, number of blocks and set the region
    # for merged dataset
    dx_level, dy_level, dz_level = [
        blocklist_level[0].dx,
        blocklist_level[0].dy,
        blocklist_level[0].dz,
    ]

    nblockx = int((dataset.xmax - dataset.xmin) / dx_level / dataset.nxb)
    nblocky = int((dataset.ymax - dataset.ymin) / dy_level / dataset.nyb)
    nblockz = int((dataset.zmax - dataset.zmin) / dz_level / dataset.nzb)

    nblockx, nblocky, nblockz = [
        value if value > 0 else 1 for value in [nblockx, nblocky, nblockz]
    ]

    region_level = library.Region(blocklist_level)

    # Actually create a merged dataset
    merged_dataset = api.create_dataset(
        nxb=nblockx * dataset.nxb,
        nyb=nblocky * dataset.nyb,
        nzb=nblockz * dataset.nzb,
        xmin=region_level.xmin,
        ymin=region_level.ymin,
        zmin=region_level.zmin,
        xmax=region_level.xmax,
        ymax=region_level.ymax,
        zmax=region_level.zmax,
    )

    blocklist_sorted = [None] * len(blocklist_level)

    for block in blocklist_level:
        iloc, jloc, kloc = block.get_relative_loc(
            origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
        )

        blocklist_sorted[iloc + nblockx * jloc + nblockx * nblocky * kloc] = block

    for varkey in varlist:
        merged_dataset.addvar(varkey, dtype=dataset.dtype[varkey])

    resources = library.Resources()

    if monitor:
        resources.display()

        print(
            f"[mem_dataset]: {round(sys.getsizeof(dataset._data.variables[varkey][:])/(2**20),2)} MB"
        )

    map_blk_to_merged_dset.nthreads = nthreads
    map_blk_to_merged_dset.monitor = monitor
    map_blk_to_merged_dset.backend = backend

    if monitor:
        time_mapping = library.Timer("[boxkit.mergeblocks.map_dataset_block]")

    map_blk_to_merged_dset(blocklist_sorted, merged_dataset, varlist)

    if monitor:
        del time_mapping

    if monitor:
        del time_mergeblocks

    return merged_dataset


@library.Action(parallel_obj=library.Block)
def map_blk_to_merged_dset(parallel_obj, merged_dataset, varlist):
    """
    map block to a merged dataset
    """
    iloc, jloc, kloc = parallel_obj.get_relative_loc(
        origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
    )

    for varkey in varlist:
        for block in merged_dataset.blocklist:
            block[varkey][
                parallel_obj.nzb * kloc : parallel_obj.nzb * (kloc + 1),
                parallel_obj.nyb * jloc : parallel_obj.nyb * (jloc + 1),
                parallel_obj.nxb * iloc : parallel_obj.nxb * (iloc + 1),
            ] = parallel_obj[varkey][:, :, :]
