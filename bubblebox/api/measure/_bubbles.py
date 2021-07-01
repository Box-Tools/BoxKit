""" Module with implemenation of region methods"""

from ...library.measure  import regionprops

from ...utilities import blockparallel

def bubbles(region,keys):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    region : Region object

    keys   : list of two keys [lsetkey, bubblekey]
             lsetkey   - stores information of level set function
             bubblekey - stores bubble information/label

    Returns
    -------
    listprops : list of properties

    """

    lsetkey,bubblekey = keys

    blockparallel(target=_block_label)(region.blocklist,lsetkey,bubblekey)

    listbubbles  = regionprops(region,bubblekey)

    return listbubbles

def _block_label(block,lsetkey,bubblekey):
    """
    tag each block using level set function
    """

    block[bubblekey] = block[lsetkey] >= 0
