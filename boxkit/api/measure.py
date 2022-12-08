""" Module with implemenation of region methods"""

import itertools
import numpy

from ..resources import stencils

from . import create


def regionprops(dataset, lsetkey, backend="serial", nthreads=1, monitor=False):
    """
    Create a list of bubbles in a region

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

    region = create.region(dataset)

    stencils.regionprops_block.nthreads = nthreads
    stencils.regionprops_block.backend = backend
    stencils.regionprops_block.monitor = monitor

    listprops = stencils.regionprops_block(region.blocklist, lsetkey, labelkey)
    listprops = list(itertools.chain.from_iterable(listprops))

    dataset.delvar(labelkey)

    return listprops
