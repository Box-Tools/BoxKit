"""Module with implemenetation of api create methods"""

from ... import library


def Dataset(data_attributes={}, block_attributes=[{}], storage="numpy-memmap"):
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
    data = library.Data(storage=storage, **data_attributes)

    blocklist = [library.Block(data, **attributes) for attributes in block_attributes]

    return library.Dataset(blocklist, data)
