""" Module with implemenation of region methods"""

from ....library.measure import regionprops

def bubbles(region,key):
    """
    regions : list of regions (Volume or Slice)

    key     : key for the variable to measure
    """

    for block in region.blocklist:
        block['bubbles'] = block[key][:] >= 0

    listprops  = regionprops(region,'bubbles')

    bubblelist = [ {'area' : props['area']} for props in listprops]

    return bubblelist
