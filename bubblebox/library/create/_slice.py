"""Module with implementation of the Slice class."""

from . import Region

class Slice(Region):
    """Derived class for a Slice."""

    type_ = 'derived'

    def __init__(self, attributes={}, blocklist=[]):
        """Initialize the Slice object and allocate the data.

        Parameters
        ----------
        attributes : dictionary
                     { 'xmin' : low  bound in x dir
                       'ymin' : low  bound in y dir
                       'zmin' : low  bound in z dir
                       'xmax' : high bound in x dir
                       'ymax' : high bound in y dir
                       'zmax' : high bound in z dir}

        blocklist  : list of block objects

        """

        super().__init__(attributes,blocklist)       
       
    def __repr__(self):
        """Return a representation of the object."""
        return ("Region:\n" +
                " - type      : {}\n".format(type(self)) +
                " - bound     : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                         self.xmax,
                                                                         self.ymin,
                                                                         self.ymax,
                                                                         self.zmin,
                                                                         self.zmax))


