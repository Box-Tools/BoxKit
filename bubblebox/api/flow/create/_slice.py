""" Module with implemenation of slice methods"""

from .... import library

def slice(dataset,**kwargs):
    """
    Create a slice from a dataset

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
    Slice object

    """
 
    slice_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                        'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in kwargs: slice_attributes[key] = kwargs[key]

    return library.create.Slice(dataset.blocklist, **slice_attributes)
