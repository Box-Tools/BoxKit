""" Module with implementation of Parallel class"""

class Parallel(object):
    """
    Parallel class
    """

    def __init__(self,**kwargs):
        """
        Constructor

        Arguments:
        ----------
        kwargs : dictionary
               { ntasks  : number of tasks,
                 process : 'loky'}
        """

        self._set_attributes(kwargs)

    def _set_attributes(self,attributes):
        """
        Private method for initialization
        """

        default_attributes = { 'ntasks'   : 1,
                               'process'  : 'loky'}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Data'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

        self._check_process()

    def _check_process(self):
        """
        Private method for intialization
        """        
        _qualified_process_list = ['loky']

        if self.process not in _qualified_process_list:
            raise NotImplementedError('Parallel backend not implemented for "{}" process'.format(self.process))
