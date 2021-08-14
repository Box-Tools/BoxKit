"""Module to read attributes from FLASH output files"""

import h5pickle as h5py

def flash(filename,uservars):
    """
    Read dataset from FLASH output file

    Parameters
    ----------
    filename : string containing file name
    uservars : list of user variables that need to be created

    Returns
    -------
    data_attributes  : dictionary containing data attributes
    block_attributes : dictionary containg block attributes
    """

    data_attributes  = {}
    block_attributes = [{}]
    
    return data_attributes,block_attributes
