"""Module with implemenetation of api create methods"""

from .. import library


def dataset(data_attributes={}, block_attributes=[{}], storage="numpy-memmap"):
    """
    Create a dataset from a file

    Parameters
    ----------
    data_attributes  : data attributes
    block_attributes : block attributes
    storage          : storage option 'disk', 'pyarrow', or 'dask'
                       default('disk')

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """
    data = library.create.Data(storage=storage, **data_attributes)

    blocklist = [
        library.create.Block(data, **attributes) for attributes in block_attributes
    ]

    return library.create.Dataset(blocklist, data)


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

    region_attributes = {
        "xmin": dataset.xmin,
        "ymin": dataset.ymin,
        "zmin": dataset.zmin,
        "xmax": dataset.xmax,
        "ymax": dataset.ymax,
        "zmax": dataset.zmax,
    }

    for key, value in attributes.items():
        region_attributes[key] = value

    return library.create.Region(dataset.blocklist, **region_attributes)


def slice(dataset, **attributes):
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

    slice_attributes = {
        "xmin": dataset.xmin,
        "ymin": dataset.ymin,
        "zmin": dataset.zmin,
        "xmax": dataset.xmax,
        "ymax": dataset.ymax,
        "zmax": dataset.zmax,
    }

    for key, value in attributes.items():
        slice_attributes[key] = value

    return library.create.Slice(dataset.blocklist, **slice_attributes)
