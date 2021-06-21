"""Module with implementation of the Block classes."""

class Block(object):
    """Default class for a Block."""

    type_ = 'default'

    def __init__(self, attributes, data):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        attributes : dictionary
                     {'tag' : block ID}

        data : data object

        """

        self._set_data(data)
        self._set_attributes(attributes)

    def __repr__(self):
        """Return a representation of the object."""
        return ("Block:\n" +
                " - type   : {}\n".format(type(self)) +
                " - size   : {} x {} x {}\n".format(self.nxb, self.nyb, self.nzb) +
                " - bound  : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                         self.xmax,
                                                                         self.ymin,
                                                                         self.ymax,
                                                                         self.zmin,
                                                                         self.zmax) +
                " - tag    : {}\n".format(self.tag))

    def __getitem__(self,key):
        """
        Get variable data
        """
        if self.tag is not None:
            return self.data[key][self.tag]
        else:
            return self.data[key]


    def __setitem__(self,key,value):
        """
        Set variable data
        """
        if self.tag is not None:
            self.data[key][self.tag] = value
        else:
            self.data[key] = value

    def _set_data(self,data):
        """
        Private method for initialization
        """
        self.data = data

    def _set_attributes(self,attributes):
        """
        Private method for intialization
        """        

        _default_attributes = {'tag' : None}

        for key in attributes:
            if key in _default_attributes:
                _default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class block'.format(key))

        for key, value in _default_attributes.items(): setattr(self, key, value)

        if self.data:
            self.xcenter = (self.xmin + self.xmax)/2.
            self.ycenter = (self.ymin + self.ymax)/2.
            self.zcenter = (self.zmin + self.zmax)/2.

            self.dx = abs(self.xmax - self.xmin) / self.nxb
            self.dy = abs(self.ymax - self.ymin) / self.nyb
            self.dz = abs(self.zmax - self.zmin) / self.nzb

            [self.dx, self.dy, self.dz] = [1. if   grid_spacing == 0. 
                                              else grid_spacing
                                              for  grid_spacing in [self.dx, self.dy, self.dz]]

    @property
    def nxb(self):
        return self.data.nxb

    @property
    def nyb(self):
        return self.data.nyb
 
    @property
    def nzb(self):
        return self.data.nxb

    @property
    def xmin(self):
        if self.tag is not None:
            return self.data.xmin[self.tag]
        else:
            return self.data.xmin

    @property
    def ymin(self):
        if self.tag is not None:
            return self.data.ymin[self.tag]
        else:
            return self.data.ymin

    @property
    def zmin(self):
        if self.tag is not None:
            return self.data.zmin[self.tag]
        else:
            return self.data.zmin

    @property
    def xmax(self):
        if self.tag is not None:
            return self.data.xmax[self.tag]
        else:
            return self.data.xmax

    @property
    def ymax(self):
        if self.tag is not None:
            return self.data.ymax[self.tag]
        else:
            return self.data.ymax

    @property
    def zmax(self):
        if self.tag is not None:
            return self.data.zmax[self.tag]
        else:
            return self.data.zmax
