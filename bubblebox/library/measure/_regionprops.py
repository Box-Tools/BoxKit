"""Module with implementation of measurement methods"""

import itertools

from skimage import measure

def regionprops(region,label):
    """
    calculate regionprops for a list of blocks
    """

    blockprops = list(map(_blockprops,region.blocklist,[label]))

    listprops = list(itertools.chain.from_iterable(blockprops))

    return listprops

def _blockprops(block,label):
    """
    calculate regionprops for a block
    """

    bwlabel    = measure.label(block[label])
    listprops  = measure.regionprops(bwlabel)

    return listprops
