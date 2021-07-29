""" Module with implemenation of region methods"""

from ....library.measure import skimeasure

from ....utilities import Process

@Process(actions=skimeasure.actions())
def bubbles(self,regionlist,lsetkey,bubblekey):
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
 
    listbubbles = self.actions['region'](regionlist,lsetkey,bubblekey)

    return listbubbles
