"""Module with implementation of measure methods"""

import skimage.measure as skimage_measure

from ...utilities import blockparallel

@blockparallel
def blockprops(block,lsetkey,labelkey):
    """
    Calculate regionprops for a block

    Parameters
    ----------
    block    : Block object

    lsetkey  : key to the level-set/binary data

    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties

    """

    block[labelkey]  =  skimage_measure.label(block[lsetkey] >= 0)

    listprops = skimage_measure.regionprops(block[labelkey].astype(int))

    listprops = [{'area' : props['area']*block.dx*block.dy*block.dz} for props in listprops]

    return listprops
