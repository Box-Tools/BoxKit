"""Module with implementation of the Grid classes."""

class grid(object):
    """Default class for the Grid."""

    type_ = 'default-grid'

    def __init__(self, attributes, blocks):
        """Initialize the Grid object and allocate the data.

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
       
        self._initialize_attributes(attributes)

        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.
  
        self._check_bounds(blocks)
        self._map_blocks(blocks)

    def __repr__(self):
        """Return a representation of the object."""
        return ("Grid:\n" +
                " - type      : {}\n".format(type(self)) +
                " - bound     : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                         self.xmax,
                                                                         self.ymin,
                                                                         self.ymax,
                                                                         self.zmin,
                                                                         self.zmax))
    def _initialize_attributes(self,attributes):
        """
        Private method for intialization
        """

        _default_attributes = {'xmin' : 0., 'ymin' : 0., 'zmin' : 0.,
                               'xmax' : 0., 'ymax' : 0., 'zmax' : 0.}

        for key in attributes:
            if key in _default_attributes:
                _default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class grid'.format(key))

        for key, value in _default_attributes.items(): setattr(self, key, value)

    def _map_blocks(self,blocks):
        """
        Private method for mapping blocks
        """
        self.blocks = [block for block in blocks]

    def _check_bounds(self,blocks):
        """
        Private method to check block bounds
        """

        min_block_bounds = [min([block.xmin for block in blocks]),
                            min([block.ymin for block in blocks]),
                            min([block.zmin for block in blocks])]

        max_block_bounds = [max([block.xmax for block in blocks]),
                            max([block.ymax for block in blocks]),
                            max([block.zmax for block in blocks])]
        
        min_grid_bounds  = [self.xmin,self.ymin,self.zmin]

        max_grid_bounds  = [self.xmax,self.ymax,self.zmax]

        min_bound_check = [grid_min >= block_min for grid_min,block_min in zip(min_grid_bounds,min_block_bounds)]

        max_bound_check = [grid_max <= block_max for grid_max,block_max in zip(max_grid_bounds,max_block_bounds)]

        if False in min_bound_check:
            raise ValueError('Cannot create grid: min bounds outside blocks scope')
        
        if False in max_bound_check:
            raise ValueError('Cannot create grid: max bounds outside blocks scope')
