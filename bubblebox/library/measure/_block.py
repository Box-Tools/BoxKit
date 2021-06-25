"""Module with implementation of measurement methods"""

from skimage import measure

def block_props(block,key):
    """
    calculate regionprops for a block
    """

    bwlabel    = measure.label(block[key][:] >= 0)
    blockprops = measure.regionprops(bwlabel)

    return blockprops
