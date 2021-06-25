"""Module with implementation of the Region classes."""

import pymorton

class Region(object):
    """Default class for the Region."""

    type_ = 'default'

    def __init__(self, attributes={}, blocks=[]):
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

        blocks     : list of block objects

        """
       
        self._set_attributes(attributes)
        self._set_blocks(blocks)

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

    def _set_blocks(self,blocks):
        """
        Private method for initialization
        """
        if blocks:
            self._check_bounds(blocks)
            self._map_blocks(blocks)        

    def _map_blocks(self,blocks):
        """
        Private method for mapping blocks
        """
        self.blocks = [block for block in blocks
                       if ((block.xmin >= self.xmin and block.xmin <= self.xmax) and
                           (block.xmax >= self.xmin and block.xmax <= self.xmax) and
                           (block.ymin >= self.ymin and block.ymin <= self.ymax) and
                           (block.ymax >= self.ymin and block.ymax <= self.ymax) and
                           (block.zmin >= self.zmin and block.zmin <= self.zmax) and
                           (block.zmax >= self.zmin and block.zmax <= self.zmax))]

    def _check_bounds(self,blocks):
        """
        Private method to check block bounds
        """

        block_xmin,block_ymin,block_zmin = [min([block.xmin for block in blocks]),
                                            min([block.ymin for block in blocks]),
                                            min([block.zmin for block in blocks])]

        block_xmax,block_ymax,block_zmax = [max([block.xmax for block in blocks]),
                                            max([block.ymax for block in blocks]),
                                            max([block.zmax for block in blocks])]

        
        min_bound_check = [region_min >= block_min for region_min,block_min in 
                                                 zip ([self.xmin,  self.ymin,  self.zmin],
                                                      [block_xmin, block_ymin, block_zmin])]

        max_bound_check = [region_max <= block_max for region_max,block_max in
                                                 zip ([self.xmax,  self.ymax,  self.zmax],
                                                      [block_xmax, block_ymax, block_zmax])]

        if False in min_bound_check:
            raise ValueError(('Cannot create region: min bounds outside blocks scope\n')+
                             ('Min region bounds: "{}"\n'.format([self.xmin,self.ymin,self.zmin]))+
                             ('Min block  bounds: "{}"\n'.format([block_xmin,block_ymin,block_zmin])))
        
        if False in max_bound_check:
            raise ValueError(('Cannot create region: max bounds outside blocks scope\n')+
                             ('Max region bounds: "{}"\n'.format([self.xmax,self.ymax,self.zmax]))+
                             ('Max block  bounds: "{}"\n'.format([block_xmax,block_ymax,block_zmax]))) 
