"""Module with implementation of decorators"""

import warnings
import copy

from . import backend

class Process(object):
    def __init__(self, target=None, actions=None):    
        self.target = target
        self.actions = copy.deepcopy(actions)

    def __call__(self,*args):
        if self.target is None:
            self.target = args[0]
            return self

        else:
            unitlist = args[0]

            args = list(args)
            args.pop(0)
            args = tuple(args)

            return self.target(self.actions,unitlist,*args)

    def clone(self):
        return copy.deepcopy(self)

class Task(object):
    def __init__(self, target=None, tasks=None, monitor=False, process='serial'):
        self.target = target
        self.tasks = tasks
        self.monitor = monitor
        self.process = process

    def __call__(self, *args):
        if self.target is None:
            self.target = args[0]
            return self

        else:
            unitlist = args[0]

            args = list(args)
            args.pop(0)
            args = tuple(args)

            return backend(self.target,self.tasks,self.monitor,self.process)(unitlist,*args)
