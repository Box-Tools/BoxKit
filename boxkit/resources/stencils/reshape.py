"""Module with implemenetation of reshape methods"""

import math
from ...library import Block, Action


@Action(unit=Block)
def map_blk_to_merged_dset(unit, merged_dataset, varkey):
    """
    map block to a merged dataset
    """
    iloc, jloc, kloc = unit.get_location(
        origin=[merged_dataset.xmin, merged_dataset.ymin, merged_dataset.zmin]
    )

    merged_dataset[varkey][
        0,
        unit.nxb * iloc : unit.nxb * (iloc + 1),
        unit.nyb * jloc : unit.nyb * (jloc + 1),
        unit.nzb * kloc : unit.nzb * (kloc + 1),
    ] = unit[varkey][:, :, :]
