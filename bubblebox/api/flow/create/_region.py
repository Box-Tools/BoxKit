""" Module with implemenation of region methods"""

from ....library.create import Region

def region(dataset, **kwargs):
    """
    Create a region from a dataset

    Parameters
    ----------

    dataset    : Dataset object
 
    kwargs : dictionary of attributes
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

    for key in kwargs: region_attributes[key] = kwargs[key]

    return Region(dataset.blocklist, **region_attributes)
