"""Module with implementation of the Region classes."""

import pymorton

class Region(object):
    """Default class for the Region."""

    type_ = 'default'

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
        self._set_blocklist(blocklist)

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

    def _set_blocklist(self,blocklist):
        """
        Private method for initialization
        """

        self._check_blocklist(blocklist)
        self._map_blocklist(blocklist)

    def _map_blocklist(self,blocklist):
        """
        Private method for mapping blocklist

        """

        if not blocklist: return

        self.blocklist = [block for block in blocklist
                          if ((block.xmin >= self.xmin and block.xmin <= self.xmax) and
                              (block.xmax >= self.xmin and block.xmax <= self.xmax) and
                              (block.ymin >= self.ymin and block.ymin <= self.ymax) and
                              (block.ymax >= self.ymin and block.ymax <= self.ymax) and
                              (block.zmin >= self.zmin and block.zmin <= self.zmax) and
                              (block.zmax >= self.zmin and block.zmax <= self.zmax))]

    def _check_blocklist(self,blocklist):
        """
        Private method to check blocklist
        """

        if not blocklist: return

        block_xmin,block_ymin,block_zmin = [min([block.xmin for block in blocklist]),
                                            min([block.ymin for block in blocklist]),
                                            min([block.zmin for block in blocklist])]

        block_xmax,block_ymax,block_zmax = [max([block.xmax for block in blocklist]),
                                            max([block.ymax for block in blocklist]),
                                            max([block.zmax for block in blocklist])]

        
        min_bound_check = [region_min >= block_min 
                           for   region_min,block_min in 
                           zip ([self.xmin,  self.ymin,  self.zmin],
                                [block_xmin, block_ymin, block_zmin])]

        max_bound_check = [region_max <= block_max 
                           for   region_max,block_max in
                           zip ([self.xmax,  self.ymax,  self.zmax],
                                [block_xmax, block_ymax, block_zmax])]

        if False in min_bound_check:
            raise ValueError(('Cannot create region: min bounds outside blocks scope\n')+
                             ('Min region bounds: "{}"\n'.format([self.xmin,self.ymin,self.zmin]))+
                             ('Min blocks  bound: "{}"\n'.format([block_xmin,block_ymin,block_zmin])))
        
        if False in max_bound_check:
            raise ValueError(('Cannot create region: max bounds outside blocks scope\n')+
                             ('Max region bounds: "{}"\n'.format([self.xmax,self.ymax,self.zmax]))+
                             ('Max blocks  bound: "{}"\n'.format([block_xmax,block_ymax,block_zmax]))) 
