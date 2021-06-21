"""Module with implementation of the Slice classes."""

import numpy
import pymorton

class Slice(object):
    """Default class for the Slice."""

    type_ = 'default'

    def __init__(self,attributes,grid):
        """Initialize the Slice object and allocate the data.

        Parameters
        ----------
        attributes : dictionary
                     { 'plane' : which plane to slice
                     }  

        grid       : grid object

        """

        self._set_grid(grid)
        self._set_attributes(attributes)        
    
    def __repr__(self):
        """Return a representation of the object."""
        return ("Slice:\n" +
                " - type      : {}\n".format(type(self)))

    def __getitem__(self,key):
        """
        """
         
        #for block in self.grid.blocks:
        #
        #    ibx,iby,ibz = pymorton.deinterleave3(block.tag)
        #
        #    ibx = ibx - self.grid.lbx['min']
        #    iby = iby - self.grid.lby['min']
        #    ibz = ibz - self.grid.lbz['min']
        #
        #    volume_data[ibx*self.grid.data.nxb:(1+ibx)*self.grid.data.nxb,
        #                iby*self.grid.data.nyb:(1+iby)*self.grid.data.nyb,
        #                ibz*self.grid.data.nzb:(1+ibz)*self.grid.data.nzb] = block[key]
        #
        return None

    def _set_grid(self,grid):
        """
        Private method for initialization
        """
        self.grid = grid
        self.size = [self.grid.lbx['total']*self.grid.data.nxb,
                     self.grid.lby['total']*self.grid.data.nyb,
                     self.grid.lbz['total']*self.grid.data.nzb] 

    def _set_attributes(self,attributes):
        """
        Private method for initialization
        """
        _default_attributes = {'plane' : 'xy'}

        for key in attributes:
            if key in _default_attributes:
                _default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class grid'.format(key))

        for key, value in _default_attributes.items(): setattr(self, key, value)

