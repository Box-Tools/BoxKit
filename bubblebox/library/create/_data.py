"""Module with implementation of the Data class."""

import numpy
import os
import string
import random

class Data(object):
    """Default class to store data"""

    type_ = "default"

    def __init__(self, attributes={}):
        """Initialize the class object

        Parameters
        ----------
        attributes : dictionary
                     { 'nblocks'   : total number of blocks
                       'nxb'       : number of grid points per block in x dir
                       'nyb'       : number of grid points per block in y dir
                       'nzb'       : number of grid points per block in z dir}

        variables  - dictionary of variables

        """

        self._set_attributes(attributes)
        self._set_data() 

    def __repr__(self):
        """
        Return a representation of the object
        """
        return ("Data:\n" +
                " - type   : {}\n".format(type(self)) +
                " - keys   : {}\n".format(self.listkeys))

    def __getitem__(self,varkey):
        """
        Get variable data
        """
        if not varkey in self.listkeys: 
            raise ValueError('Variable "{}" does not exist in "{}"'.format(varkey,self.listkeys))
        else:
            return self.variables[varkey]


    def __setitem__(self,varkey,value):
        """
        Set variable data
        """
        if not varkey in self.listkeys:
            raise ValueError('Variable "{}" does not exist in "{}"'.format(varkey,self.listkeys))

        else:
            self.variables[varkey] = value

    def _set_attributes(self,attributes):
        """
        Private method for intialization
        """

        default_attributes = {'nblocks'   : 1,              
                              'inputfile' : None,
                              'variables' : {},
                                    'nxb' : 1, 'nyb' : 1, 'nzb' : 1}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Data'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

    def _set_data(self):
        """
        Private method for setting new data
        """

        self.listkeys  = list(self.variables.keys())
        self.memmap = None
        self._create_memmap()

    def _create_memmap(self):
        """
        Create a memory map for numpy arrays
        """

        emptykeys = [varkey for varkey in self.listkeys if self.variables[varkey] == None]
      
        if not emptykeys: return

        namerandom  = ''.join(random.choice(string.ascii_lowercase) for i in range(5)) 
        self.memmap = "".join(['./memmap_',namerandom])

        try:
            os.mkdir(self.memmap)
        except FileExistsError:
            pass

        for varkey in emptykeys:
            outputfile  = os.path.join(self.memmap,varkey)
            outputshape = (self.nblocks,self.nxb,self.nyb,self.nzb)
            self.variables[varkey] = numpy.memmap(outputfile, dtype=float, shape=outputshape, mode='w+')
