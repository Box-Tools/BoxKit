"""Module with implemenetation of api methods"""

import sys

from .. import library
from .. import api


def mergeblocks(dataset, varlist, level=1, nthreads=1, monitor=False, backend="serial"):
    """
    Reshaped dataset at a level
    """
    if monitor:
        time_mergeblocks = library.Timer("[boxkit.mergeblocks]")

    if isinstance(varlist, str):
        varlist = [varlist]

    blocklist_level = []
    for block in dataset.blocklist:
        if block.level == level:
            blocklist_level.append(block)

    if not blocklist_level:
        raise ValueError(
            f"[boxkit.mergeblocks]: level={level} does not exist in input dataset"
        )

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
        print(
            f'[cpu_count]: {resources["cpu_count"]}',
            f'[cpu_avail]: {resources["cpu_avail"]}',
            f'[mem_avail]: {resources["mem_avail"]} GB',
            f'[cpu_usage]: {resources["cpu_usage"]}%',
            f'[mem_usage]: {resources["mem_usage"]}%',
        )

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


@library.Action(unit=library.Block)
def map_blk_to_merged_dset(unit, merged_dataset, varlist):
    """
    map block to a merged dataset
    """
    iloc, jloc, kloc = unit.get_relative_loc(
        origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
    )

    for varkey in varlist:
        for block in merged_dataset.blocklist:
            block[varkey][
                unit.nzb * kloc : unit.nzb * (kloc + 1),
                unit.nyb * jloc : unit.nyb * (jloc + 1),
                unit.nxb * iloc : unit.nxb * (iloc + 1),
            ] = unit[varkey][:, :, :]
