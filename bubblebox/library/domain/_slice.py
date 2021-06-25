"""Module with implementation of the Slice classes."""

import numpy
import pymorton

class Slice(object):
    """Default class for the Slice."""

    type_ = 'default'

    def __init__(self,attributes={},blocks=[]):
        """Initialize the Slice object and allocate the data.

        Parameters
        ----------
        attributes : dictionary
                     {'plane' : which plane to slice, 
                      'imin'  : min bound in i dir,
                      'jmin'  : min bound in j dir,
                      'imax'  : max bound in i dir,
                      'jmax'  : max bound in j dir}  

        blocks     : list of blocks

        """

        self._set_attributes(attributes)        
        self._set_blocks(blocks)
   
    def __repr__(self):
        """Return a representation of the object."""
        return ("Slice:\n" +
                " - type      : {}\n".format(type(self)) +
                " - plane     : {}\n".format(self.plane) +
                " - bound     : [{}, {}] x [{}, {}]\n".format(self.imin,
                                                              self.imax,
                                                              self.jmin,
                                                              self.jmax))

    def _set_attributes(self,attributes):
        """
        Private method for initialization
        """
        default_attributes = {'plane': 'y',
                              'imin' : 0., 'jmin' : 0.,
                              'imax' : 0., 'jmax' : 0.}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Slice'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

        self.icenter = (self.imin + self.imax)/2.
        self.jcenter = (self.jmin + self.jmax)/2.

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
                       if ((block.xmin >= self.imin and block.xmin <= self.imax) and
                           (block.xmax >= self.imin and block.xmax <= self.imax) and
                           (block.zmin >= self.jmin and block.zmin <= self.jmax) and
                           (block.zmax >= self.jmin and block.zmax <= self.jmax))]

    def _check_bounds(self,blocks):
        """
        Private method to check block bounds
        """

        block_xmin,block_zmin = [min([block.xmin for block in blocks]),
                                 min([block.zmin for block in blocks])]

        block_xmax,block_zmax = [max([block.xmax for block in blocks]),
                                 max([block.zmax for block in blocks])]
        
        min_bound_check = [slice_min >= block_min for slice_min,block_min in 
                                                  zip ([self.imin,  self.jmin],
                                                       [block_xmin, block_zmin])]

        max_bound_check = [slice_max <= block_max for slice_max,block_max in
                                                  zip ([self.imax,  self.jmax],
                                                       [block_xmax, block_zmax])]

        if False in min_bound_check:
            raise ValueError(('Cannot create slice: min bounds outside blocks scope\n')+
                             ('Min slice bounds: "{}"\n'.format([self.imin,self.jmin]))+
                             ('Min block  bounds: "{}"\n'.format([block_xmin,block_zmin])))
        
        if False in max_bound_check:
            raise ValueError(('Cannot create slice: max bounds outside blocks scope\n')+
                             ('Max slice bounds: "{}"\n'.format([self.imax,self.jmax]))+
                             ('Max block  bounds: "{}"\n'.format([block_xmax,block_zmax]))) 
