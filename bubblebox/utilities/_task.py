"""Module with implementation of Task decorator"""
import copy

from . import Backend

class Task(object):
    """
    """
    def __init__(self, target=None, nthreads=None, monitor=False, backend='serial', process=None):
        self.target = target
        self.nthreads = nthreads
        self.monitor = monitor
        self.backend = backend
        self.process = process
 
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
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def CustomCall(self,*args):
        unitlist,args = self.TopArg(*args)
        return Backend(self.target,self.nthreads,self.monitor,self.backend)(self,unitlist,*args)

