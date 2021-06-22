# Import libraries
import h5py
from ... import library

class Dataset(object):
    """Class for storing Dataset info"""

    type_ = "default"

    def __init__(self,blocks,inputfile):
        """Constructor for Dataset

        Parameters
        ----------

        blocks : list of block objects

        inputfile : handle for hdf5 file

        """
        self.blocks    = blocks
        self.inputfile = inputfile

    def __repr__(self):
        """Return a representation of the object."""
        return ("Data:\n" +
                " - type : {}\n".format(type(self)) +
                " - file : {}\n".format(self.inputfile))

def read_dataset(filename):
    """
    """
    # Read the hdf5 file
    inputfile = h5py.File(filename,'r')

    # Create data object
    lblocks = inputfile['numbox'][0]*inputfile['numbox'][1]*inputfile['numbox'][2]
    data_attributes = {'lblocks' : lblocks,
                       'nxb'     : inputfile['sizebox'][0],
                       'nyb'     : inputfile['sizebox'][1],
                       'nzb'     : inputfile['sizebox'][2],
                       'xmin'    : inputfile['boundbox/min'][:,0],
                       'ymin'    : inputfile['boundbox/min'][:,1],
                       'zmin'    : inputfile['boundbox/min'][:,2],
                       'xmax'    : inputfile['boundbox/max'][:,0],
                       'ymax'    : inputfile['boundbox/max'][:,1],
                       'zmax'    : inputfile['boundbox/max'][:,2]}

    data3D = library.Data(attributes=data_attributes, variables=inputfile['quantities'])

    # Create block objects
    block_attributes = [{'nxb'  : data3D.nxb,
                         'nyb'  : data3D.nyb,
                         'nzb'  : data3D.nzb,
                         'xmin' : data3D.xmin[lblock],
                         'ymin' : data3D.ymin[lblock],
                         'zmin' : data3D.zmin[lblock],
                         'xmax' : data3D.xmax[lblock],
                         'ymax' : data3D.ymax[lblock],
                         'zmax' : data3D.zmax[lblock],
                         'tag'  : lblock} for lblock in range(data3D.lblocks)] 

    blocks3D = [library.Block(attributes=block_attr,data=data3D) for block_attr in block_attributes]

    return Dataset(blocks3D,inputfile)

def create_grid(grid_attributes,dataset):
    """
    """
    grid3D = library.Grid(attributes=grid_attributes,blocks=dataset.blocks)

    return Dataset(grid3D.blocks,dataset.inputfile)

