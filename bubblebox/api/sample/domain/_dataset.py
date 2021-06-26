"""Module with implemenetation of Dataset methods"""

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
