"""Module with implemenetation of Dataset class and methods"""

from .... import library

from ....resources.read import default,flash

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

    read = {'default' : default, 'flash' : flash}

    data_attributes,block_attributes = read[source](filename,uservars)

    data_attributes['storage'] = storage

    data = library.create.Data(**data_attributes)

    blocklist = [library.create.Block(data, **attributes) for attributes in block_attributes]

    return library.create.Dataset(blocklist,data)
