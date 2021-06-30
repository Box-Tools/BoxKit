"""Module with implemenetation of Dataset class"""

import shutil

class Dataset(object):
    """API class for storing Dataset info"""

    type_ = "default"

    def __init__(self,blocklist=[],data=None):
        """Constructor for Dataset

        Parameters
        ----------
        blocklist : list of block objects

        data      : Data object

        """
        self._map_blocklist(blocklist)
        self._map_data(data)

    def __repr__(self):
        """Return a representation of the object."""
        return ("Dataset:\n" +
                " - type  : {}\n".format(type(self)) +
                " - file  : {}\n".format(self.inputfile)+
                " - keys  : {}\n".format(self.listkeys) +
                " - bound : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                     self.xmax,
                                                                     self.ymin,
                                                                     self.ymax,
                                                                     self.zmin,
                                                                     self.zmax))

    def _map_blocklist(self,blocklist):
        """
        Private method for initialization
        """
        if not blocklist: return

        self.blocklist  = blocklist

        self.xmin,self.ymin,self.zmin = [min([block.xmin for block in self.blocklist]),
                                         min([block.ymin for block in self.blocklist]),
                                         min([block.zmin for block in self.blocklist])]

        self.xmax,self.ymax,self.zmax = [max([block.xmax for block in self.blocklist]),
                                         max([block.ymax for block in self.blocklist]),
                                         max([block.zmax for block in self.blocklist])]

    def _map_data(self,data):
        """
        Private method for initialization
        """
        if not data: return

        self.listkeys   = data.listkeys
        self.inputfile  = data.inputfile
        self.memmap     = data.memmap

    def close(self):
        """
        Clean up the dataset and close it
        """

        if self.memmap:
            try:
                shutil.rmtree(self.memmap)
            except:
                pass

        if self.inputfile: self.inputfile.close()
