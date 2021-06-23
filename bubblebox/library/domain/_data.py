"""Module with implementation of the Data classes."""

import numpy

class Data(object):
    """Default class to store data"""

    type_ = "default"

    def __init__(self, attributes={}, variables={}):
        """Initialize the class object

        Parameters
        ----------
        attributes : dictionary
                     { 'lblocks' : total number of blocks
                       'nxb'     : number of grid points per block in x dir
                       'nyb'     : number of grid points per block in y dir
                       'nzb'     : number of grid points per block in z dir}

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
                " - keys   : {}\n".format(self.keys))

    def __getitem__(self,key):
        """
        Get variable data
        """
        if not key in self.keys: 
            raise ValueError('Variable "{}" does not exist in "{}"'.format(key,self.keys))
        else:
            return self.variables[key]


    def __setitem__(self,key,value):
        """
        Set variable data
        """
        if not key in self.keys:
            raise ValueError('Variable "{}" does not exist in "{}"'.format(key,self.keys))

        else:
            self.variables[key] = value

    def _set_attributes(self,attributes):
        """
        Private method for intialization
        """

        default_attributes = {'lblocks' : 1,              
                                  'nxb' : 1, 'nyb' : 1, 'nzb' : 1}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class block'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

    def _set_variables(self,variables):
        """
        Private method for intialization
        """

        self.variables = variables
        self.keys      = list(self.variables.keys())

        self._set_data()

    def _set_data(self):
        """
        Private method for setting new data
        """

        empty_keys = [key for key in self.keys if self.variables[key] == None]

        for key in empty_keys: self.variables[key] = numpy.zeros([lblocks,nxb,nyb,nzb])
