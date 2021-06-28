""" Module with implemenation of region methods"""

from ...library.measure import regionprops

import functools
import multiprocessing as parallel

def bubbles(region,keys):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    regions   : list of regions (Volume or Slice)


    keys      : list of two keys [lsetkey, bubblekey]
                lsetkey   - stores information of level set function
                bubblekey - stores bubble information/label

    Returns
    -------
    listprops : list of properties

    """

    lsetkey,bubblekey = keys

    blocktags  = list(map(functools.partial(_tag_block_bubbles,lsetkey,bubblekey),region.blocklist))

    listprops  = regionprops(region,bubblekey)

    bubblelist = [ {'area' : props['area']} for props in listprops]

    return bubblelist

def _tag_block_bubbles(lsetkey,bubblekey,block):
    """
    tag each block using level set function
    """

    block[bubblekey] = block[lsetkey] >= 0
