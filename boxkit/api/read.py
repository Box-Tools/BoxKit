"""Module with implemenetation of api read methods"""

from .. import library

from ..resources import read


def Dataset(filename, source="test-sample", storage="numpy", server=None):
    """
    Create a dataset from a file

    Parameters
    ----------
    filename : string containing file name
    source   : string identifying source/format of the file
               'test-sample' : method to create sample dataset for BoxKit API tests
               'flash'  : method to create FLASH dataset
    storage  : storage option 'disk', 'pyarrow', or 'dask'
               default('disk')

    server : server dictionary

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """

    data_attributes, block_attributes = read.options[source](filename, server)

    data = library.Data(storage=storage, **data_attributes)

    blocklist = [library.Block(data, **attributes) for attributes in block_attributes]

    return library.Dataset(blocklist, data)
