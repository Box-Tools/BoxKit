"""Module with implementation of Task utility"""

import copy

from . import Backend

class Task(object):
    """
    """
    def __init__(self, target=None, nthreads=None, monitor=False, backend='serial', actions=None, unit=None):
        self.target = target
        self.nthreads = nthreads
        self.monitor = monitor
        self.backend = backend
        self.actions = actions
        self.unit = unit

    def __call__(self,*args):
        if self.target is None:
            self.target = args[0]
            return self

        else: 
            return self.CustomCall(*args)

    def TopArg(self,*args):
        top_arg = args[0]

        args = list(args)
        args.pop(0)
        args = tuple(args)

        self._unit_check(top_arg)

        return top_arg,args

    def CustomCall(self,*args):
        unitlist,args = self.TopArg(*args)
        return Backend(self.target,self.nthreads,self.monitor,self.backend)(self,unitlist,*args)

    def clone(self):
        return copy.copy(self)

    def _unit_check(self,unitlist):
        
        if(type(unitlist) is not list): raise ValueError('[Task] Top argument must be a list of units')

        for unit in unitlist:
            if(type(unit) is not self.unit): 
                raise ValueError('[Task] Unit type not consistent.' +
                                 'Expected "{}" but got "{}"'.format(self.unit,type(unit)))

