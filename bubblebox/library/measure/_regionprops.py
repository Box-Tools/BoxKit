"""Module with implementation of measure methods"""

import itertools
import skimage.measure as skimage_measure
import functools
import multiprocessing as parallel

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

    initlabel   = list(map(functools.partial(_init_block_label,labelkey),region.blocklist))
    updatelabel = list(map(functools.partial(_update_block_label,labelkey),region.blocklist))
    blockprops  = list(map(functools.partial(_get_block_props,labelkey),region.blocklist))

    listprops   = list(itertools.chain.from_iterable(blockprops))

    return listprops

def _init_block_label(labelkey,block):
    """
    Label a block using skimage.measure.label

    Parameters
    ----------
    block    : Block object

    labelkey : variable containing label

    """

    block[labelkey]  =  skimage_measure.label(block[labelkey])

def _update_block_label(labelkey,block):
    """
    Update a block label before measurement

    Parameters
    ----------
    block    : Block object

    labelkey : variable containing label

    """
    pass

def _get_block_props(labelkey,block):
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

    listprops = skimage_measure.regionprops(block[labelkey].astype(int))

    return listprops
