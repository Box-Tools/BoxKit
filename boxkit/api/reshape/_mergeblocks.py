"""Module with implemenetation of api reshape methods"""

import sys
import math

from ... import library
from ...library import Block, Action, Timer, Resources


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
        merged_dataset.addvar(varkey, dtype=dataset.dtype[varkey])

        resources = Resources()
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
        print(
            f"[mem_merged_dataset]: {round(sys.getsizeof(merged_dataset._data.variables[varkey][:])/(2**20),2)} MB"
        )

        map_blk_to_merged_dset.nthreads = nthreads
        map_blk_to_merged_dset.monitor = monitor
        map_blk_to_merged_dset.backend = backend

        time_mapping = Timer("[boxkit.stencils.map_dataset_block]")
        map_blk_to_merged_dset(blocklist_sorted, merged_dataset, varkey)
        del time_mapping

    del time_mergeblocks
    return merged_dataset


@Action(unit=Block)
def map_blk_to_merged_dset(unit, merged_dataset, varkey):
    """
    map block to a merged dataset
    """
    iloc, jloc, kloc = unit.get_location(
        origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
    )

    # TODO - this statement behaves differently for
    # test datasets vs desired way - investigate. It maybe because
    # test datasets were not constructured properly and maybe its time
    # to build a new test datasets after all
    #
    # for test datasets
    # merged_dataset[varkey][
    #     0,
    #     unit.nxb * iloc : unit.nxb * (iloc + 1),
    #     unit.nyb * jloc : unit.nyb * (jloc + 1),
    #     unit.nzb * kloc : unit.nzb * (kloc + 1),
    # ] = unit[varkey][:, :, :]
    #
    # desired
    merged_dataset[varkey][
        0,
        unit.nzb * kloc : unit.nzb * (kloc + 1),
        unit.nyb * jloc : unit.nyb * (jloc + 1),
        unit.nxb * iloc : unit.nxb * (iloc + 1),
    ] = unit[varkey][:, :, :]
