""" Module with implemenation of region methods"""

from ....library import measure

import ..create

from ....utilities import Process

@Process(actions=measure.skimeasure())
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

@Process(actions=measure.skimeasure())
def bubbles_test(self,dataframes,lsetkey,**attributes):
    """
    Create a list of bubbles in a region

    Parameters
    ----------
    dataframes : list of Region objects

    lsetkey    : key containing level-set/binary data

    Returns
    -------
    listbubbles : list of bubble properties
    """

    

    regionlist = [create.region(dataset, **attributes) for dataset in dataframes]
    

 
    listbubbles = self.actions['region'](regionlist,lsetkey,bubblekey)

    return listbubbles

