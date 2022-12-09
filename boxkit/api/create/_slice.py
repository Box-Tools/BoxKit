"""Module with implemenetation of api create methods"""

from ... import library


def Slice(dataset, **attributes):
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

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.Slice(blocklist, **slice_attributes)
