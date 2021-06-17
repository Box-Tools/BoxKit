"""Module with implementation of the Data classes."""

class data(object):
    """Default class for a Data packet"""

    type_ = "default"

    def __init__(self, variables):
        """Initialize the class object

        Parameters
        ----------
        variables - dictionary

        """

        self.variables = variables
        self.keys      = list(self.variables.keys())


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

