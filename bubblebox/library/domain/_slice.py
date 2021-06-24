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

    def __getitem__(self,key):
        """
        """                
        return None

    def _set_attributes(self,attributes):
        """
        Private method for initialization
        """
        default_attributes = {'plane': 'xy',
                              'imin' : 0., 'jmin' : 0.,
                              'imax' : 0., 'jmax' : 0.}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Slice'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

    def _set_blocks(self,blocks):
        """
        Private method for initialization
        """
        return None
