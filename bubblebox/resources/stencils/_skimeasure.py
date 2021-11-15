"""Module with implementation of measure methods"""

import itertools
import skimage.measure as skimage_measure

from ...library.utilities import Action
from ...library.create    import Region,Block

def skimeasure():
    """
    Public method to create a dictionary of actions
    """

    tasks = {'skimeasure' : {'region' : skimeasure_region.copy(),
                             'block'  : skimeasure_block.copy() }}

    for action in tasks['skimeasure'].values(): action.tasks = tasks

    return tasks

@Action(unit=Region)
def skimeasure_region(self,unit,lsetkey,labelkey):
    """
    Measure properties for a region

    Parameters
    ----------
    unit     : Region object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """

    listprops = self.tasks['skimeasure']['block'](unit.blocklist,lsetkey,labelkey)

    listprops = list(itertools.chain.from_iterable(listprops))

    return listprops

@Action(unit=Block)
def skimeasure_block(self,unit,lsetkey,labelkey):
    """
    Measure properties for a block

    Parameters
    ----------
    unit     : Block object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """

    unit[labelkey][:,:,:] = skimage_measure.label(unit[lsetkey] >= 0)

    listprops = skimage_measure.regionprops(unit[labelkey].astype(int))

    listprops = [{'area' : props['area']*unit.dx*unit.dy*unit.dz} for props in listprops]

    return listprops
