"""Module with implemenetation of api/flow create methods"""

from .. import library

from ..resources import read

def dataset(filename,uservars=[],source='default',storage='disk'):
    """
    Create a dataset from a file

    Parameters
    ----------
    filename : string containing file name 
    uservars : list of vars user wants to add to the dataset
    source   : string identifying source/format of the file
               'sample' : method to create sample dataset for BubbleBox API tests
               'flash'  : method to create FLASH dataset
    storage  : storage option 'disk', 'pyarrow', or 'dask'
               default('disk')

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """

    data_attributes,block_attributes = read.options[source](filename,uservars)

    data = library.create.Data(storage=storage, **data_attributes)

    blocklist = [library.create.Block(data, **attributes) for attributes in block_attributes]

    return library.create.Dataset(blocklist,data)


def region(dataset, **attributes):
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

    return library.create.Region(dataset.blocklist, **region_attributes)


def slice(dataset,**attributes):
    """
    Create a slice from a dataset

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
    Slice object
    """
 
    slice_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                        'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in attributes: slice_attributes[key] = attributes[key]

    return library.create.Slice(dataset.blocklist, **slice_attributes)
