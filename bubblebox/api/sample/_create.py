""" Module with implemenation of create methods"""

from ... import library

def create_volume(dataset,attributes={}):
    """
    """
    volume_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                         'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in attributes: volume_attributes[key] = attributes[key]

    volume = library.domain.Volume(attributes=volume_attributes,blocks=dataset.blocks)

    return volume

def create_slice(dataset,attributes={}):
    """
    """
    slice_attributes = {'plane' : 'y',
                        'imin'  : dataset.xmin, 'jmin' : dataset.zmin,
                        'imax'  : dataset.xmax, 'jmax' : dataset.zmax}

    for key in attributes: slice_attributes[key] = attributes[key]

    slice = library.domain.Slice(attributes=slice_attributes,blocks=dataset.blocks)

    return slice

