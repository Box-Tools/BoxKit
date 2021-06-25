"""Module with implementation of measurement methods"""

import itertools

from . import block_props

def region_props(region,key):
    """
    calculate regionprops for a list of blocks
    """

    allblockprops = list(map(block_props,region.blocks,[key]))

    regionprops = list(itertools.chain.from_iterable(allblockprops))

    return regionprops
