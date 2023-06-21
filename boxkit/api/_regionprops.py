""" Module with implemenation of measure methods"""

import itertools
import skimage.measure as skimage_measure

from boxkit import api  # pylint: disable=cyclic-import
from boxkit.library import Action  # pylint: disable=cyclic-import


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

    listprops = skimage_props_blk(
        (block for block in region.blocklist), lsetkey, labelkey
    )
    listprops = list(itertools.chain.from_iterable(listprops))

    dataset.delvar(labelkey)

    return listprops


@Action
def skimage_props_blk(block, lsetkey, labelkey):
    """
    Measure properties for a block

    Parameters
    ----------
    block     : Block object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """

    block[labelkey][:, :, :] = skimage_measure.label(block[lsetkey] >= 0)

    listprops = skimage_measure.regionprops(block[labelkey].astype(int))

    # proplist = ["area", "centroid", "equivalent_diameter_area"]
    proplist = ["area"]

    # listprops = [
    #    {"area": props["area"] * block.dx * block.dy * block.dz} for props in listprops
    # ]

    listprops = [{key: props[key] for key in proplist} for props in listprops]

    return listprops
