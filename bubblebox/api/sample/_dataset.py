# Import libraries
import h5py
from ... import library

class Dataset(object):
    """Class for storing Dataset info"""

    type_ = "default"

    def __init__(self,blocks,inputfile,keys):
        """Constructor for Dataset

        Parameters
        ----------

        blocks : list of block objects

        inputfile : handle for hdf5 file

        """
        self.blocks    = blocks
        self.inputfile = inputfile
        self.keys      = keys

    def __repr__(self):
        """Return a representation of the object."""
        return ("Data:\n" +
                " - type : {}\n".format(type(self)) +
                " - file : {}\n".format(self.inputfile)+
                " - keys : {}\n".format(self.keys))

def read_dataset(filename):
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
                         'tag'  : lblock} for lblock in range(data3D.lblocks)] 

    blocks3D = [library.domain.Block(attributes=block_attr,data=data3D) for block_attr in block_attributes]

    return Dataset(blocks3D,inputfile,data3D.keys)

def create_grid(grid_attributes,dataset):
    """
    """
    return library.domain.Grid(attributes=grid_attributes,blocks=dataset.blocks)
