""" Module with implemenation of region methods"""

from ...library.measure  import regionprops

from ...parallel import Parallel

def bubbles(region,keys,nparallel=1):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    regions   : list of regions (Volume or Slice)


    keys      : list of two keys [lsetkey, bubblekey]
                lsetkey   - stores information of level set function
                bubblekey - stores bubble information/label

    nparallel : number of parallel jobs

    Returns
    -------
    listprops : list of properties

    """

    lsetkey,bubblekey = keys

    Parallel(nparallel).map(_block_label,region.blocklist,lsetkey,bubblekey)

    listprops  = regionprops(region,bubblekey,nparallel)

    bubblelist = [ {'area' : props['area']} for props in listprops]

    return bubblelist

def _block_label(block,lsetkey,bubblekey):
    """
    tag each block using level set function
    """

    block[bubblekey] = block[lsetkey] >= 0
