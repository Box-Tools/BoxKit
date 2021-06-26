""" Module with implemenation of region methods"""

from ...library.measure import regionprops

def bubbles(region,key):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    regions : list of regions (Volume or Slice)

    key     : key for the variable containing level set function to identify the bubble

    user needs to specifiy 'bubbles' in uservars when creating dataset to use this functionality

    Returns
    -------
    listprops : list of properties

    """

    for block in region.blocklist:
        block['bubbles'] = block[key][:] >= 0

    listprops  = regionprops(region,'bubbles')

    bubblelist = [ {'area' : props['area']} for props in listprops]

    return bubblelist
