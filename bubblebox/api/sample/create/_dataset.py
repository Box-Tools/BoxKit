"""Module with implemenetation of Dataset methods"""

import h5py

from ....library.domain import Data,Block

from ..domain import Dataset

def dataset3D(filename,variables=[]):
    """
    """
    # Read the hdf5 file
    inputfile = h5py.File(filename,'r')

    # Extract data
    numblocks = inputfile['numbox'][0]*inputfile['numbox'][1]*inputfile['numbox'][2]
    nxb       = inputfile['sizebox'][0]
    nyb       = inputfile['sizebox'][1]
    nzb       = inputfile['sizebox'][2]
    xmin      = inputfile['boundbox/min'][:,0]
    ymin      = inputfile['boundbox/min'][:,1]
    zmin      = inputfile['boundbox/min'][:,2]
    xmax      = inputfile['boundbox/max'][:,0]
    ymax      = inputfile['boundbox/max'][:,1]
    zmax      = inputfile['boundbox/max'][:,2]

    variables = dict(zip(variables,[None]*len(variables)))

    variables.update(inputfile['quantities'])

    # Create data object
    data_attributes = {'numblocks': numblocks,
                       'nxb'      : nxb,
                       'nyb'      : nyb,
                       'nzb'      : nzb}

    data = Data(data_attributes,variables)

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
                         'tag'  : lblock if data.numblocks > 1 else None} for lblock in range(data.numblocks)] 

    blocklist = [Block(attributes,data) for attributes in block_attributes]

    return Dataset(blocklist,inputfile,data.keys)

def dataset2D(filename,variables=[]):
    """
    """
    # Read the hdf5 file
    inputfile = h5py.File(filename,'r')

    # Extract data
    numblocks = inputfile['numbox'][0]*inputfile['numbox'][1]
    nxb       = inputfile['sizebox'][0]
    nzb       = inputfile['sizebox'][1]
    xmin      = inputfile['boundbox/min'][:,0]
    zmin      = inputfile['boundbox/min'][:,1]
    xmax      = inputfile['boundbox/max'][:,0]
    zmax      = inputfile['boundbox/max'][:,1]

    variables = dict(zip(variables,[None]*len(variables)))

    variables.update(inputfile['quantities'])

    # Create data object
    data_attributes = {'numblocks': numblocks,
                       'nxb'      : nxb,
                       'nzb'      : nzb}

    data = Data(data_attributes,variables)

    # Create block objects
    block_attributes = [{'nxb'  : nxb,
                         'nzb'  : nzb,
                         'xmin' : xmin[lblock],
                         'zmin' : zmin[lblock],
                         'xmax' : xmax[lblock],
                         'zmax' : zmax[lblock],
                         'tag'  : lblock if data.numblocks > 1 else None} for lblock in range(data.numblocks)] 

    blocklist = [Block(attributes,data) for attributes in block_attributes]

    return Dataset(blocklist,inputfile,data.keys)
