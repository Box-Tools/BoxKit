""" Module with implemenation of region methods"""

from ...library.measure import regionprops

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

    for block in region.blocklist:
        block[bubblekey] = block[lsetkey][:] >= 0

    listprops  = regionprops(region,bubblekey)

    bubblelist = [ {'area' : props['area']} for props in listprops]

    return bubblelist
