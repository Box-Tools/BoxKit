"""Module with implemenetation of Dataset class"""

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
        self.blocklist = []
        self.xmin,self.ymin,self.zmin = [1e10]*3
        self.xmax,self.ymax,self.zmax = [-1e10]*3

        if not blocklist: return

        self.blocklist  = blocklist

        for block in self.blocklist:
            self.xmin = min(self.xmin,block.xmin)
            self.ymin = min(self.ymin,block.ymin)
            self.zmin = min(self.zmin,block.zmin)
         
            self.xmax = max(self.xmax,block.xmax)
            self.ymax = max(self.ymax,block.ymax)
            self.zmax = max(self.zmax,block.zmax)
 
    def _map_data(self,data):
        """
        Private method for initialization
        """
        self._data = None

        if not data: return

        self._data = data

    @property
    def nblocks(self):
        return self._data.nblocks

    def addvar(self,varkey):
        self._data.addvar(varkey)

    def delvar(self,varkey):
        self._data.delvar(varkey)

    def purge(self,purgeflag='all'):
        """
        Clean up the dataset and close it
        """
        self._data.purge(purgeflag)
