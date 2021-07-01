"""Module with implementation of the Region class."""

class Region(object):
    """Base class for a Region."""

    type_ = 'base'

    def __init__(self, attributes={}, blocklist=[]):
        """Initialize the Region object and allocate the data.

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
       
        self._set_attributes(attributes)
        self._map_blocklist(blocklist)

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

    def _set_attributes(self,attributes):
        """`
        Private method for intialization
        """

        default_attributes = {'xmin' : 0., 'ymin' : 0., 'zmin' : 0.,
                              'xmax' : 0., 'ymax' : 0., 'zmax' : 0.}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Region'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.

    def _map_blocklist(self,blocklist):
        """
        Private method for initialization
        """
        self.blocklist = []

        if not blocklist: return

        self.blocklist = [block for block in blocklist if self._in_collision(block)]

        self._update_bounds()

    def _in_collision(self,block):
        """
        Check if a block is in collision with the region
        """        
        xcollision  = abs(self.xcenter-block.xcenter)-(self.xmax-self.xmin)/2.-(block.xmax-block.xmin)/2. <= 0.
        ycollision  = abs(self.ycenter-block.ycenter)-(self.ymax-self.ymin)/2.-(block.ymax-block.ymin)/2. <= 0.
        zcollision  = abs(self.zcenter-block.zcenter)-(self.zmax-self.zmin)/2.-(block.zmax-block.zmin)/2. <= 0.

        incollision = xcollision and ycollision and zcollision 

        return incollision

    def _update_bounds(self):
        """
        Update block bounds using the blocklist
        """
        if not self.blocklist: raise ValueError('Region is empty and outside scope of Blocks\n')

        for block in self.blocklist:
            self.xmin = min(self.xmin,block.xmin)
            self.ymin = min(self.ymin,block.ymin)
            self.zmin = min(self.zmin,block.zmin)
         
            self.xmax = max(self.xmax,block.xmax)
            self.ymax = max(self.ymax,block.ymax)
            self.zmax = max(self.zmax,block.zmax)
 
        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.
