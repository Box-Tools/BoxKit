"""Module with implementation of measure methods"""

import skimage.measure as skimage_measure

from ...library import Action
from ...library import Block


@Action(unit=Block)
def skimage_props_blk(unit, lsetkey, labelkey):
    """
    Measure properties for a block

    Parameters
    ----------
    unit     : Block object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """

    unit[labelkey][:, :, :] = skimage_measure.label(unit[lsetkey] >= 0)

    listprops = skimage_measure.regionprops(unit[labelkey].astype(int))

    listprops = [
        {"area": props["area"] * unit.dx * unit.dy * unit.dz} for props in listprops
    ]

    return listprops
