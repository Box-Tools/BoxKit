"""Module with implemenetation of read methods """

import h5py
from ... import library
from .   import Dataset

def read_dataset3D(filename):
    """
    """
    # Read the hdf5 file
    inputfile = h5py.File(filename,'r')

    # Extract data
    lblocks = inputfile['numbox'][0]*inputfile['numbox'][1]*inputfile['numbox'][2]
    nxb     = inputfile['sizebox'][0]
    nyb     = inputfile['sizebox'][1]
    nzb     = inputfile['sizebox'][2]
    xmin    = inputfile['boundbox/min'][:,0]
    ymin    = inputfile['boundbox/min'][:,1]
    zmin    = inputfile['boundbox/min'][:,2]
    xmax    = inputfile['boundbox/max'][:,0]
    ymax    = inputfile['boundbox/max'][:,1]
    zmax    = inputfile['boundbox/max'][:,2]
    quants  = inputfile['quantities']

    # Create data object
    data_attributes = {'lblocks' : lblocks,
                       'nxb'     : nxb,
                       'nyb'     : nyb,
                       'nzb'     : nzb}

    data3D = library.domain.Data(attributes=data_attributes, variables=quants)

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
                         'tag'  : lblock if data3D.lblocks > 1 else None} for lblock in range(data3D.lblocks)] 

    blocks3D = [library.domain.Block(attributes=block_attr,data=data3D) for block_attr in block_attributes]

    return Dataset(blocks3D,inputfile,data3D.keys)

def read_dataset2D(filename):
    """
    """
    # Read the hdf5 file
    inputfile = h5py.File(filename,'r')

    # Extract data
    lblocks = inputfile['numbox'][0]*inputfile['numbox'][1]
    nxb     = inputfile['sizebox'][0]
    nyb     = inputfile['sizebox'][1]
    xmin    = inputfile['boundbox/min'][:,0]
    ymin    = inputfile['boundbox/min'][:,1]
    xmax    = inputfile['boundbox/max'][:,0]
    ymax    = inputfile['boundbox/max'][:,1]
    quants  = inputfile['quantities']

    # Create data object
    data_attributes = {'lblocks' : lblocks,
                       'nxb'     : nxb,
                       'nyb'     : nyb}

    data2D = library.domain.Data(attributes=data_attributes, variables=quants)

    # Create block objects
    block_attributes = [{'nxb'  : nxb,
                         'nyb'  : nyb,
                         'xmin' : xmin[lblock],
                         'ymin' : ymin[lblock],
                         'xmax' : xmax[lblock],
                         'ymax' : ymax[lblock],
                         'tag'  : lblock if data2D.lblocks > 1 else None} for lblock in range(data2D.lblocks)] 

    blocks2D = [library.domain.Block(attributes=block_attr,data=data2D) for block_attr in block_attributes]

    return Dataset(blocks2D,inputfile,data2D.keys)
