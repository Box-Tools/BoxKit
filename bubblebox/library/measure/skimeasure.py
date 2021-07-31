"""Module with implementation of measure methods"""

import itertools

import skimage.measure as skimage_measure

from ...utilities import Task, TaskUnit

def actions(): return {task: eval(task) for task in ['region','block']}

@TaskUnit
def region(self,unit,lsetkey,labelkey):
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
    listprops = self.actions['block'](unit.blocklist,lsetkey,labelkey)

    listprops = list(itertools.chain.from_iterable(listprops))

    return listprops

@TaskUnit
def block(self,unit,lsetkey,labelkey):
    """
    Measure properties for a unit

    Parameters
    ----------
    unit     : Block object

    lsetkey  : key to the level-set/binary data

    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties

    """
    unit[labelkey] = skimage_measure.label(unit[lsetkey] >= 0)

    listprops = skimage_measure.regionprops(unit[labelkey].astype(int))

    listprops = [{'area' : props['area']*unit.dx*unit.dy*unit.dz} for props in listprops]

    return listprops
