"""Module with implementation of the Block classes."""

class Block(object):
    """Default class for a Block."""

    type_ = 'default'

    def __init__(self, attributes, data):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        attributes : dictionary
                     { 'nxb'  : number of grid points in x dir
                       'nyb'  : number of grid points in y dir
                       'nzb'  : number of grid points in z dir
                       'xmin' : low  bound in x dir
                       'ymin' : low  bound in y dir
                       'zmin' : low  bound in z dir
                       'xmax' : high bound in x dir
                       'ymax' : high bound in y dir
                       'zmax' : high bound in z dir
                       'tag'  : block ID for reference }

        data       : data object

        """

        self._initialize_attributes(attributes)

        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.

        self.dx = abs(self.xmax - self.xmin) / self.nxb
        self.dy = abs(self.ymax - self.ymin) / self.nyb
        self.dz = abs(self.zmax - self.zmin) / self.nzb

        [self.dx, self.dy, self.dz] = [1. if   grid_spacing == 0. 
                                          else grid_spacing
                                          for  grid_spacing in [self.dx, self.dy, self.dz]]

        self.data = data

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
                " - data   : {} \n".format(self.data))

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

    def _initialize_attributes(self,attributes):
        """
        Private subroutine for intialization
        """

        _default_attributes = {'nxb'  : 1 , 'nyb'  : 1,  'nzb'  : 1,
                               'xmin' : 0., 'ymin' : 0., 'zmin' : 0.,
                               'xmax' : 0., 'ymax' : 0., 'zmax' : 0.,
                               'tag'  : None}

        for key in attributes:
            if key in _default_attributes:
                _default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class block'.format(key))

        for key, value in _default_attributes.items(): setattr(self, key, value)

