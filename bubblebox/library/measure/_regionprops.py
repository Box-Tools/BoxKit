"""Module with implementation of measure methods"""

import itertools
import skimage.measure as skimage_measure

from ...parallel import Parallel

def regionprops(region,labelkey,nparallel=1):
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

    Parallel(nparallel).map(_block_label_bw,region.blocklist,labelkey)

    blockprops = [_block_props(block,labelkey) for block in region.blocklist]

    listprops  = list(itertools.chain.from_iterable(blockprops))

    return listprops

def _block_label_bw(block,labelkey):
    """
    Label a block using skimage.measure.label

    Parameters
    ----------
    block    : Block object

    labelkey : variable containing label

    """

    block[labelkey]  =  skimage_measure.label(block[labelkey])

def _block_props(block,labelkey):
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
