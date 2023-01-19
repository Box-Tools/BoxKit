"""Module with implemenetation of api methods"""

import sys

from .. import library
from .. import api
from ..library import Action


def mergeblocks(
    dataset, varlist, nthreads=1, batch="auto", monitor=False, backend="serial"
):
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

    # Handle errors, compute level of the first
    # block and raise error if not same for the rest
    level = dataset.blocklist[0].level
    for block in dataset.blocklist:
        if block.level != level:
            raise ValueError(
                f"[boxkit.mergeblocks] All blocks must be at level {level}"
            )

    # Compute number of blocks in each direction
    nblockx = int((dataset.xmax - dataset.xmin) / dataset.blocklist[0].dx / dataset.nxb)
    nblocky = int((dataset.ymax - dataset.ymin) / dataset.blocklist[0].dy / dataset.nyb)
    nblockz = int((dataset.zmax - dataset.zmin) / dataset.blocklist[0].dz / dataset.nzb)

    nblockx, nblocky, nblockz = [
        value if value > 0 else 1 for value in [nblockx, nblocky, nblockz]
    ]

    # Create a merged dataset
    merged_dataset = api.create_dataset(
        nblockx=1,
        nblocky=1,
        nblockz=1,
        nxb=nblockx * dataset.nxb,
        nyb=nblocky * dataset.nyb,
        nzb=nblockz * dataset.nzb,
        xmin=dataset.xmin,
        ymin=dataset.ymin,
        zmin=dataset.zmin,
        xmax=dataset.xmax,
        ymax=dataset.ymax,
        zmax=dataset.zmax,
        storage="numpy-memmap",
    )

    blocklist_sorted = [None] * len(dataset.blocklist)

    for block in dataset.blocklist:
        iloc, jloc, kloc = block.get_relative_loc(
            origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
        )

        blocklist_sorted[iloc + nblockx * jloc + nblockx * nblocky * kloc] = block

    for varkey in varlist:
        merged_dataset.addvar(varkey, dtype=dataset.dtype[varkey])

    resources = library.Resources()

    if monitor:
        resources.display()

    map_blk_to_merged_dset.nthreads = nthreads
    map_blk_to_merged_dset.monitor = monitor
    map_blk_to_merged_dset.backend = backend
    map_blk_to_merged_dset.batch = batch

    if monitor:
        time_mapping = library.Timer("[boxkit.mergeblocks.map_dataset_block]")

    map_blk_to_merged_dset(
        (blk_sorted for blk_sorted in blocklist_sorted), merged_dataset, varlist
    )

    if monitor:
        del time_mapping

    if monitor:
        del time_mergeblocks

    return merged_dataset


@Action
def map_blk_to_merged_dset(blk_sorted, merged_dataset, varlist):
    """
    map block to a merged dataset
    """
    iloc, jloc, kloc = blk_sorted.get_relative_loc(
        origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
    )

    for varkey in varlist:
        for block in merged_dataset.blocklist:
            block[varkey][
                blk_sorted.nzb * kloc : blk_sorted.nzb * (kloc + 1),
                blk_sorted.nyb * jloc : blk_sorted.nyb * (jloc + 1),
                blk_sorted.nxb * iloc : blk_sorted.nxb * (iloc + 1),
            ] = blk_sorted[varkey][:, :, :]
