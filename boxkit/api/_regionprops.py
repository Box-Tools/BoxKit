""" Module with implemenation of measure methods"""

import itertools
import skimage.measure as skimage_measure

from .. import api
from .. import library


def regionprops(dataset, lsetkey, backend="serial", nthreads=1, monitor=False):
    """
    Parameters
    ----------
    dataset : Dataset object
    lsetkey : key containing level-set/binary data

    Returns
    -------
    listprops : list of bubble properties
    """

    labelkey = "bwlabel"
    dataset.addvar(labelkey, dtype=int)

    region = api.create_region(dataset)

    skimage_props_blk.nthreads = nthreads
    skimage_props_blk.backend = backend
    skimage_props_blk.monitor = monitor

    listprops = skimage_props_blk(region.blocklist, lsetkey, labelkey)
    listprops = list(itertools.chain.from_iterable(listprops))

    dataset.delvar(labelkey)

    return listprops


@library.Action(unit=library.Block)
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