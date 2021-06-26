"""Module with implemenetation of Dataset class and methods"""

from ...library.create import Data,Block

from ...resources.read import sample,flash

def dataset(filename,uservars=[],source='sample'):
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

    read = {'sample' : sample, 'flash' : flash}

    data_attributes,block_attributes,inputfile,variables = read[source](filename,uservars)

    data      = Data(data_attributes,variables)
    blocklist = [Block(attributes,data) for attributes in block_attributes]

    return Dataset(blocklist,inputfile,data.keys)

class Dataset(object):
    """API class for storing Dataset info"""

    type_ = "default"

    def __init__(self,blocklist,inputfile,datakeys):
        """Constructor for Dataset

        Parameters
        ----------
        blocklist : list of block objects

        inputfile : handle for hdf5 file

        """
        self.blocklist = blocklist
        self.inputfile = inputfile
        self.datakeys  = datakeys

        self.xmin,self.ymin,self.zmin = [min([block.xmin for block in self.blocklist]),
                                         min([block.ymin for block in self.blocklist]),
                                         min([block.zmin for block in self.blocklist])]

        self.xmax,self.ymax,self.zmax = [max([block.xmax for block in self.blocklist]),
                                         max([block.ymax for block in self.blocklist]),
                                         max([block.zmax for block in self.blocklist])]

    def __repr__(self):
        """Return a representation of the object."""
        return ("Dataset:\n" +
                " - type  : {}\n".format(type(self)) +
                " - file  : {}\n".format(self.inputfile)+
                " - keys  : {}\n".format(self.datakeys) +
                " - bound : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                     self.xmax,
                                                                     self.ymin,
                                                                     self.ymax,
                                                                     self.zmin,
                                                                     self.zmax))
