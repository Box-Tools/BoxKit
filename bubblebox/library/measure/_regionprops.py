"""Module with implementation of measurement methods"""

import itertools

import skimage.measure as skimage_measure

def regionprops(region,keylabel):
    """
    calculate regionprops for a list of blocks
    """

    initlabel   = list(map(_init_block_label,   region.blocklist, [keylabel]))
    updatelabel = list(map(_update_block_label, region.blocklist, [keylabel]))
    blockprops  = list(map(_get_block_props,    region.blocklist, [keylabel]))

    listprops   = list(itertools.chain.from_iterable(blockprops))

    return listprops

def _init_block_label(block,keylabel):
    """
    label a block
    """

    block[keylabel]  =  skimage_measure.label(block[keylabel])

    return None

def _update_block_label(block,keylabel):
    """
    update block label
    """
    return None

def _get_block_props(block,keylabel):
    """
    calculate regionprops for a block
    """

    listprops = skimage_measure.regionprops(block[keylabel])

    return listprops
