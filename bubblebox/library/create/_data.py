"""Module with implementation of the Data class."""

import numpy

class Data(object):
    """Default class to store data"""

    type_ = "default"

    def __init__(self, attributes={}, variables={}):
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
        self._set_variables(variables) 

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

        default_attributes = {'nblocks' : 1,              
                              'nxb' : 1, 'nyb' : 1, 'nzb' : 1}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Data'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

    def _set_variables(self,variables):
        """
        Private method for intialization
        """

        self.variables = variables
        self.listkeys  = list(self.variables.keys())

        self._set_data()

    def _set_data(self):
        """
        Private method for setting new data
        """

        emptykeys = [varkey for varkey in self.listkeys if self.variables[varkey] == None]

        for varkey in emptykeys: self.variables[varkey] = numpy.zeros([self.nblocks,self.nxb,self.nyb,self.nzb])
