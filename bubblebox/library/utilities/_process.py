"""Module with implementation of Process utility"""

import copy

class Process(object):
    """Default class for a Process."""

    type_ = 'default'

    def __init__(self, target=None, stencils=None):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        target : target function
        tasks  : dictionary of tasks
        """
        super().__init__()
        self.target = target

        self.tasks = dict()

        [self.tasks.update(module()) for module in stencils]
       
    def __call__(self,*args):
        """
        Call wrapper for process

        If target is None, define the target, else call the target
        """
        if self.target is None:
            self.target = args[0]
            return self

        else:
            return self.target(self,*args)

    def clone(self):
        """
        Clone process
        """
        return copy.deepcopy(self)
