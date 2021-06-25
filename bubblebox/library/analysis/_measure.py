"""Module with implementation of measurement methods"""

from skimage import measure

def BlockProps(block,key):
    """
    """

    bwlabel    = measure.label(block[key][:] >= 0)
    blockprops = measure.regionprops(bwlabel)

    return blockprops
