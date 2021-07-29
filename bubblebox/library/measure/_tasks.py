"""Module with implementation of measure methods"""

import itertools

from ...utilities import Task

class Properties(object):

    @Task
    def region(unit,lsetkey,labelkey):
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
        listprops = Properties.block(unit.blocklist,lsetkey,labelkey)

        listprops = list(itertools.chain.from_iterable(listprops))

        return listprops

    @Task
    def block(unit,lsetkey,labelkey):
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
