"""Module with implemenetation of reshape methods"""

import math
from ...library import Block, Action


@Action(unit=Block)
def map_blk_to_merged_dset(unit, merged_dataset, varkey):
    iloc, jloc, kloc = [
        math.ceil(
            (unit.xmin - merged_dataset.xmin) / (unit.xmax - unit.xmin + 1e-13)
        ),
        math.ceil(
            (unit.ymin - merged_dataset.ymin) / (unit.ymax - unit.ymin + 1e-13)
        ),
        math.ceil(
            (unit.zmin - merged_dataset.zmin) / (unit.zmax - unit.zmin + 1e-13)
        ),
    ]

    merged_dataset[varkey][
        0,
        unit.nxb * iloc : unit.nxb * (iloc + 1),
        unit.nyb * jloc : unit.nyb * (jloc + 1),
        unit.nzb * kloc : unit.nzb * (kloc + 1),
    ] = unit[varkey][:, :, :]
