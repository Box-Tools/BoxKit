""" Module with implemenation of region methods"""

import itertools

from ...library.measure import blockprops

from ...utilities import regionparallel

@regionparallel
def bubbles(region,keys):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    region : Region object

    keys   : list of two keys [lsetkey, bubblekey]
             lsetkey   - key containing level-set/binary data
             bubblekey - key to store scratch data

    Returns
    -------
    listbubbles : list of bubble properties
    """

    lsetkey,bubblekey = keys

    listprops = blockprops(region.blocklist,lsetkey,bubblekey)

    listbubbles = list(itertools.chain.from_iterable(listprops))

    return listbubbles
