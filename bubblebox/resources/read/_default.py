"""Module to read attributes from default files"""

import h5py

def default(filename,uservars):
    """
    Read dataset from BubbleBox default file

    Parameters
    ----------
    filename : string containing file name
    uservars : list of user variables that need to be created

    Returns
    -------
    data_attributes  : dictionary containing data attributes
    block_attributes : dictionary containg block attributes
    inputfile        : hdf5 handle for input file
    variables        : dictionary containing variables

    """

    # Read the hdf5 file
    inputfile = h5py.File(filename,'r')

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

    variables = dict(zip(uservars,[None]*len(uservars)))

    variables.update(inputfile['quantities'])

    # Create data object
    data_attributes = {'nblocks' : nblocks,
                       'nxb'     : nxb,
                       'nyb'     : nyb,
                       'nzb'     : nzb}

    # Create block objects
    block_attributes = [{'nxb'  : nxb,
                         'nyb'  : nyb,
                         'nzb'  : nzb,
                         'xmin' : xmin[lblock],
                         'ymin' : ymin[lblock],
                         'zmin' : zmin[lblock],
                         'xmax' : xmax[lblock],
                         'ymax' : ymax[lblock],
                         'zmax' : zmax[lblock],
                         'tag'  : lblock if nblocks > 1 else None} for lblock in range(nblocks)]

    return data_attributes,block_attributes,inputfile,variables
