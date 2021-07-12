"""Module with implementation of measure methods"""

import itertools

from ...utilities import parallel

from . import blockprops

@parallel
def regionprops(region,lsetkey,labelkey):
    """
    Measure properties for a region

    Parameters
    ----------
    region : Region object

    lsetkey  : key to the level-set/binary data

    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """

    listprops = blockprops(region.blocklist,lsetkey,labelkey)

    listprops = list(itertools.chain.from_iterable(listprops))

    return listprops
