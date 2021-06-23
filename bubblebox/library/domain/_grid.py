"""Module with implementation of the Grid classes."""

import pymorton

class Grid(object):
    """Default class for the Grid."""

    type_ = 'default'

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
       
        self._set_attributes(attributes)
        self._set_blocks(blocks)

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
                raise ValueError('Attribute "{}" not present in class grid'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.

    def _set_blocks(self,blocks):
        """
        Private method for initialization
        """
        self.blocks = []

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
        """

        self.lbx,self.lby,self.lbz = [dict(),dict(),dict()]
 
        self.lbx['min'],self.lby['min'],self.lbz['min']  = \
                      [min([pymorton.deinterleave3(block.tag)[0] for block in self.blocks]),
                       min([pymorton.deinterleave3(block.tag)[1] for block in self.blocks]),
                       min([pymorton.deinterleave3(block.tag)[2] for block in self.blocks])]

        self.lbx['max'],self.lby['max'],self.lbz['max'] = \
                      [max([pymorton.deinterleave3(block.tag)[0] for block in self.blocks]),
                       max([pymorton.deinterleave3(block.tag)[1] for block in self.blocks]),
                       max([pymorton.deinterleave3(block.tag)[2] for block in self.blocks])]

        self.lbx['total'] = self.lbx['max']-self.lbx['min']+1
        self.lby['total'] = self.lby['max']-self.lby['min']+1
        self.lbz['total'] = self.lbz['max']-self.lbz['min']+1

        """

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
            print('Min grid  bounds: "{}"\n',min_grid_bounds)
            print('Min block bounds: "{}"\n',min_block_bounds)
            raise ValueError('Cannot create grid: min bounds outside blocks scope')
        
        if False in max_bound_check:
            print('Max grid  bounds: "{}"\n',max_grid_bounds)
            print('Max block bounds: "{}"\n',max_block_bounds)
            raise ValueError('Cannot create grid: max bounds outside blocks scope')

