""" Module with implemenation of region methods"""

from ...library.measure  import regionprops

from ...utilities import parallel

def bubbles(region,keys):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    regions : list of regions (Volume or Slice)


    keys    : list of two keys [lsetkey, bubblekey]
              lsetkey   - stores information of level set function
              bubblekey - stores bubble information/label

    Returns
    -------
    listprops : list of properties

    """

    lsetkey,bubblekey = keys

    _block_label(region.blocklist,lsetkey,bubblekey)

    listprops  = regionprops(region,bubblekey)

    bubblelist = [ {'area' : props['area']} for props in listprops]

    return bubblelist

@parallel
def _block_label(block,lsetkey,bubblekey):
    """
    tag each block using level set function
    """

    block[bubblekey] = block[lsetkey] >= 0
