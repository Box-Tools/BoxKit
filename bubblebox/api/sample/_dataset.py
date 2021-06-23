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

        self.xmin,self.ymin,self.zmin = [min([block.xmin for block in self.blocks]),
                                         min([block.ymin for block in self.blocks]),
                                         min([block.zmin for block in self.blocks])]

        self.xmax,self.ymax,self.zmax = [max([block.xmax for block in self.blocks]),
                                         max([block.ymax for block in self.blocks]),
                                         max([block.zmax for block in self.blocks])]

    def __repr__(self):
        """Return a representation of the object."""
        return ("Dataset:\n" +
                " - type  : {}\n".format(type(self)) +
                " - file  : {}\n".format(self.inputfile)+
                " - keys  : {}\n".format(self.keys) +
                " - bound : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                         self.xmax,
                                                                         self.ymin,
                                                                         self.ymax,
                                                                         self.zmin,
                                                                         self.zmax))
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

def create_grid(dataset,attributes={}):
    """
    """
    grid_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                       'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in attributes: grid_attributes[key] = attributes[key]

    return library.domain.Grid(attributes=grid_attributes,blocks=dataset.blocks)
