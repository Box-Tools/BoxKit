"""Module to read attributes from FLASH output files"""

import h5pickle as h5py

def read_flash(filename):
    """
    Read dataset from FLASH output file

    Parameters
    ----------
    filename : string containing file name

    Returns
    -------
    data_attributes  : dictionary containing data attributes
    block_attributes : dictionary containg block attributes
    """

    data_attributes  = {}
    block_attributes = [{}]
    
    return data_attributes,block_attributes
