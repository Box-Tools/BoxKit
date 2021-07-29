"""Module with implementation of Process decorator"""

import copy

class Process(object):
    """
    """
    def __init__(self, target=None, actions=None):    
        """
        """
        self.target = target

        self.actions = actions() 
        for key in self.actions:
            self.actions[key].process = self

    def __call__(self,*args):
        if self.target is None:
            self.target = args[0]
            return self

        else:
            return self.target(self,*args)

    def clone(self):
        return copy.deepcopy(self)
