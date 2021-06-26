""" Module with implemenation of region methods"""

from ...library.create import Region

def region(dataset,attributes={}):
    """
    Create a region from a dataset

    Parameters
    ----------

    dataset    : Dataset object
 
    attributes : dictionary of attributes
                 { 'xmin' : low x bound
                   'ymin' : low y bound
                   'zmin' : low z bound
                   'xmax' : high x bound
                   'ymax' : high y bound
                   'zmax' : high z bound }

    Returns
    -------
    Region object

    """
 
    region_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                         'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in attributes: region_attributes[key] = attributes[key]

    return Region(region_attributes,dataset.blocklist)
