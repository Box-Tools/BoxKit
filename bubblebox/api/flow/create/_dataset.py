"""Module with implemenetation of Dataset class and methods"""

from ....library.create import Data,Block,Dataset

from ....resources.read import default,flash

def dataset(filename,uservars=[],source='default'):
    """
    Create a dataset from a file

    Parameters
    ----------

    filename : string containing file name 

    uservars : list of vars user wants to add to the dataset

    source   : string identifying source/format of the file
               'sample' : method to create sample dataset for BubbleBox API tests
               'flash'  : method to create FLASH dataset

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """

    read = {'default' : default, 'flash' : flash}

    data_attributes,block_attributes = read[source](filename,uservars)

    data      = Data(data_attributes) 
    blocklist = [Block(attributes,data) for attributes in block_attributes]

    return Dataset(blocklist,data)
