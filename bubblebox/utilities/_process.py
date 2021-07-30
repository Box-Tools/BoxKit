"""Module with implementation of Process decorator"""

import copy

class Process(object):
    """
    """
    def __init__(self, target=None, actions=None):    
        """
        """
        self.target = target
        self.actions = actions

    def __call__(self,*args):
        if self.target is None:
            self.target = args[0]
            return self

        else:
            return self.target(self,*args)

    @property
    def actions(self):
        return self._actions


    @actions.setter
    def actions(self,value):

        self._actions = value

        for task in self.actions.values():
            task.actions = self._actions

    def clone(self):
        return copy.deepcopy(self)
