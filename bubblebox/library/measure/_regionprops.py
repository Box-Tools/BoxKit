"""Module with implementation of measure methods"""

import itertools

import skimage.measure as skimage_measure

def regionprops(region,labelkey):
    """
    Calculate regionprops for a list of blocks

    Parameters
    ----------
    region   : Region object

    labelkey : variable containing label

    Returns
    -------
    listprops : list of properties

    """

    initlabel   = list(map(_init_block_label,   region.blocklist, [labelkey]))
    updatelabel = list(map(_update_block_label, region.blocklist, [labelkey]))
    blockprops  = list(map(_get_block_props,    region.blocklist, [labelkey]))

    listprops   = list(itertools.chain.from_iterable(blockprops))

    return listprops

def _init_block_label(block,labelkey):
    """
    Label a block using skimage.measure.label

    Parameters
    ----------
    block    : Block object

    labelkey : variable containing label

    """

    block[labelkey]  =  skimage_measure.label(block[labelkey])

    return None

def _update_block_label(block,labelkey):
    """
    Update a block label before measurement

    Parameters
    ----------
    block    : Block object

    labelkey : variable containing label

    """

    return None

def _get_block_props(block,labelkey):
    """
    Calculate regionprops for a block

    Parameters
    ----------
    block    : Block object

    labelkey : variable containing label

    Returns
    -------
    listprops : list of properties

    """

    listprops = skimage_measure.regionprops(block[labelkey])

    return listprops
