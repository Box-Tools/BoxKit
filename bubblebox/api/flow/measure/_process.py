""" Module with implemenation of region methods"""

from .... import library

from ....utilities import Process

@Process(actions=library.measure.Properties())
def bubbles(actions,regionlist,lsetkey,bubblekey):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    regionlist : list of Region objects

    lsetkey    : key containing level-set/binary data

    bubblekey  : key to store scratch data

    Returns
    -------
    listbubbles : list of bubble properties
    """
 
    listbubbles = actions.region(regionlist,lsetkey,bubblekey)

    return listbubbles
