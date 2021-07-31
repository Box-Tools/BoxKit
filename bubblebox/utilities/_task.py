"""Module with implementation of Task utility"""

import copy

from . import Backend

class Task(object):
    """
    """
    def __init__(self, target=None, nthreads=None, monitor=False, backend='serial', actions=None):
        self.target = target
        self.nthreads = nthreads
        self.monitor = monitor
        self.backend = backend
        self.actions = actions

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
        return top_arg,args

    def clone(self):
        return copy.copy(self)

    def CustomCall(self,*args):
        pass

class TaskUnit(Task):
    """
    """
    def CustomCall(self,*args):
        unitlist,args = self.TopArg(*args)
        return Backend(self.target,self.nthreads,self.monitor,self.backend)(self,unitlist,*args)

