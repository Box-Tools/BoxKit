"""Module with implementation of Jacobi algorithm"""

from ...library.utilities import Action
from ...library.create    import Region,Block

def jacobi():
    """
    Public method to create a dictionary of actions
    """
    tasks = {'region' : jacobi_region.copy(),
             'block'  : jacobi_block.copy() }

    for action in tasks.values(): action.tasks = tasks

    return tasks

@Action(unit=Region)
def jacobi_region(self,unit,lsetkey,labelkey):
    """
    Parameters
    ----------
    unit     : Region object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """
    pass

@Action(unit=Block)
def jacobi_block(self,unit,lsetkey,labelkey):
    """
    Parameters
    ----------
    unit     : Block object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """
    pass
