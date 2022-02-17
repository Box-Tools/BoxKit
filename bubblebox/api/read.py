"""Module with implemenetation of api read methods"""

from .. import library

from ..resources import read


def dataset(filename, source="default", storage="numpy"):
    """
    Create a dataset from a file

    Parameters
    ----------
    filename : string containing file name
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

    data_attributes, block_attributes = read.options[source](filename)

    data = library.create.Data(storage=storage, **data_attributes)

    blocklist = [
        library.create.Block(data, **attributes) for attributes in block_attributes
    ]

    return library.create.Dataset(blocklist, data)
