"""Module with implemenetation of reshape methods"""

import math
from ...library import Block, Action


def reshape():
    """
    Public method to create a dictionary of actions
    """

    tasks = {
        "reshape": {
            "block": reshape_block.copy(),
        }
    }

    for action in tasks["reshape"].values():
        action.tasks = tasks

    return tasks


@Action(unit=Block, backend="loky")
def reshape_block(self, unit, dataset_reshaped, varkey):
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
