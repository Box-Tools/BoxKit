"""Module with implementation of measure methods"""

import itertools

import skimage.measure as skimage_measure

def regionprops(region,keylabel):
    """
    Calculate regionprops for a list of blocks

    Parameters
    ----------
    region   : Region object

    keylabel : variable containing label

    Returns
    -------
    listprops : list of properties

    """

    initlabel   = list(map(_init_block_label,   region.blocklist, [keylabel]))
    updatelabel = list(map(_update_block_label, region.blocklist, [keylabel]))
    blockprops  = list(map(_get_block_props,    region.blocklist, [keylabel]))

    listprops   = list(itertools.chain.from_iterable(blockprops))

    return listprops

def _init_block_label(block,keylabel):
    """
    Label a block using skimage.measure.label

    Parameters
    ----------
    block    : Block object

    keylabel : variable containing label

    """

    block[keylabel]  =  skimage_measure.label(block[keylabel])

    return None

def _update_block_label(block,keylabel):
    """
    Update a block label before measurement

    Parameters
    ----------
    block    : Block object

    keylabel : variable containing label

    """

    return None

def _get_block_props(block,keylabel):
    """
    Calculate regionprops for a block

    Parameters
    ----------
    block    : Block object

    keylabel : variable containing label

    Returns
    -------
    listprops : list of properties

    """

    listprops = skimage_measure.regionprops(block[keylabel])

    return listprops
