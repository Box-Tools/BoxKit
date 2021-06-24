"""Module with implementation of Dataset classes """

class Dataset(object):
    """API class for storing Dataset info"""

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
