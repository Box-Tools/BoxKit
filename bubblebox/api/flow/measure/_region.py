""" Module with implemenation of region methods"""

from ....library.measure import regionprops

def bubbles(regionlist,keys): #TODO find better way to deal with progress
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    progress : Progress object to measure advancement

    region   : list of Region objects

    keys     : list of two keys [lsetkey, bubblekey]
               lsetkey   - key containing level-set/binary data
               bubblekey - key to store scratch data

    Returns
    -------
    listbubbles : list of bubble properties
    """

    lsetkey,bubblekey = keys

    listbubbles = regionprops(regionlist,lsetkey,bubblekey)

    return listbubbles
