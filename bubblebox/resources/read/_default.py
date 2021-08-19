"""Module to read attributes from default files"""

import h5pickle as h5py

def read_default(filename):
    """
    Read dataset from BubbleBox default file

    Parameters
    ----------
    filename : string containing file name

    Returns
    -------
    data_attributes  : dictionary containing data attributes
    block_attributes : dictionary containg block attributes
    """

    # Read the hdf5 file
    inputfile = h5py.File(filename,'r',skip_cache=False)

    # Extract data
    nblocks   = inputfile['numbox'][0]*inputfile['numbox'][1]*inputfile['numbox'][2]
    nxb       = inputfile['sizebox'][0]
    nyb       = inputfile['sizebox'][1]
    nzb       = inputfile['sizebox'][2]
    xmin      = inputfile['boundbox/min'][:,0]
    ymin      = inputfile['boundbox/min'][:,1]
    zmin      = inputfile['boundbox/min'][:,2]
    xmax      = inputfile['boundbox/max'][:,0]
    ymax      = inputfile['boundbox/max'][:,1]
    zmax      = inputfile['boundbox/max'][:,2]

    variables = dict()
    variables.update(inputfile['quantities'])

    # Create data object
    data_attributes = {'nblocks'   : int(nblocks),
                       'nxb'       : int(nxb),
                       'nyb'       : int(nyb),
                       'nzb'       : int(nzb),
                       'inputfile' : inputfile,
                       'variables' : variables}

    # Create block objects
    block_attributes = [{'nxb'  : int(nxb),
                         'nyb'  : int(nyb),
                         'nzb'  : int(nzb),
                         'xmin' : xmin[lblock],
                         'ymin' : ymin[lblock],
                         'zmin' : zmin[lblock],
                         'xmax' : xmax[lblock],
                         'ymax' : ymax[lblock],
                         'zmax' : zmax[lblock],
                         'tag'  : lblock} for lblock in range(nblocks)]

    return data_attributes,block_attributes
