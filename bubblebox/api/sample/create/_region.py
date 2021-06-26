""" Module with implemenation of region methods"""

from ....library.domain  import Region

def region(dataset,attributes={}):
    """
    dataset    : Dataset object
 
    attributes : dictionary of attributes
    """
 
    region_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                         'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in attributes: region_attributes[key] = attributes[key]

    return Region(region_attributes,dataset.blocklist)
