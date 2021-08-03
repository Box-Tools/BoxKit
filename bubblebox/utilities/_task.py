"""Module with implementation of Task utility"""

import copy

from . import Backend

class Task(object):
    """Default class for a Task."""

    type_ = 'default'

    def __init__(self, target=None, nthreads=None, monitor=False, backend='serial', actions=None, unit=None):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        target   : function/task operates on an unit ---> def target(unit, *args)
                   actual call passes unitlist ---> target(unitlist, *args)

        nthreads : number of nthreads (only relevant for parallel operations)

        monitor  : flag (True or False) to show progress bar for task

        backend  : 'serial', 'loky', 'dask'
 
        actions  : dictionary of actions

        unit     : unit type
        """
        self.target   = target
        self.nthreads = nthreads
        self.monitor  = monitor
        self.backend  = backend
        self.actions  = actions
        self.unit     = unit

    def __call__(self,*args):
        """
        Call wrapper
        """
        if self.target is None:
            self.target = args[0]
            return self

        else: 
            return self.customCall(*args)

    def _check_unitlist(self,unitlist):
        """
        Check if unitlist matches the unit type
        """
        if(type(unitlist) is not list): raise ValueError('[Task] Top argument must be a list of units')

        for unit in unitlist:
            if(type(unit) is not self.unit): 
                raise ValueError('[Task] Unit type not consistent.' +
                                 'Expected "{}" but got "{}"'.format(self.unit,type(unit)))

    def topArg(self,*args):
        """
        Method to get top argument from *args
        """
        top_arg = args[0]

        args = list(args)
        args.pop(0)
        args = tuple(args)

        self._check_unitlist(top_arg)

        return top_arg,args

    def customCall(self,*args):
        """
        Custom call signature 
        """
        unitlist,args = self.topArg(*args)
        return Backend(self.target,self.nthreads,self.monitor,self.backend)(self,unitlist,*args)

    def copy(self):
        """
        custom copy method
        """
        return copy.copy(self)
